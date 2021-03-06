from controlr.events.models import Event
from datetime import datetime
import pytz
from controlr.utils.helpers import get_minutes_from_td, get_total_minutes
from controlr.devices.models import Device
from django.db import connection
from copy import deepcopy
from datetime import timedelta


def fetch_device_usage_timeseries(frequency, start_ts, end_ts, device_ids, building_id):

    if device_ids is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT date_trunc(%s, timestamp) ts, string_agg(device_id || \'|\' || state_change::varchar || \'|\' || timestamp::varchar, \',\' ORDER BY timestamp DESC) timestamps FROM events_event WHERE timestamp BETWEEN %s AND %s AND device_id IN %s GROUP BY ts',
                [frequency, start_ts, end_ts, tuple(device_ids)]
            )

            return [row for row in cursor.fetchall()]
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT date_trunc(%s, timestamp) ts, string_agg(device_id || \'|\' || state_change::varchar || \'|\' || timestamp::varchar, \',\' ORDER BY timestamp DESC) timestamps FROM events_event WHERE timestamp BETWEEN %s AND %s AND building_id=%s GROUP BY ts',
                [frequency, start_ts, end_ts, building_id]
            )

            return [row for row in cursor.fetchall()]


def get_latest_device_states(building_id, device_ids, timestamp):

    if device_ids is not None:
        if len(device_ids) == 1:
            device_ids = f'({device_ids[0]})'
        else:
            device_ids = tuple(device_ids)

        latest_devices_states = Event.objects.raw(
            'SELECT id, device_id, timestamp FROM ( SELECT id, device_id, timestamp, ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY timestamp DESC) AS rn FROM events_event WHERE timestamp <= \'{}\' AND device_id IN {} GROUP BY id, device_id ) AS t WHERE rn <= 1 ORDER BY id, rn'.format(
                timestamp, device_ids)
        )
    else:
        latest_devices_states = Event.objects.raw(
            f'SELECT id, device_id, timestamp FROM ( SELECT id, device_id, timestamp, ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY timestamp DESC) AS rn FROM events_event WHERE timestamp <= \'{timestamp}\' AND building_id = {building_id} GROUP BY id, device_id ) AS t WHERE rn <= 1 ORDER BY id, rn'
        )

    return latest_devices_states


def get_devices_usage(building_id, device_ids, start_ts, end_ts):

    # Add timezone information to the start and end timestamps

    events = Event.objects.filter(
        building_id=building_id,
        timestamp__range=(start_ts, end_ts)
    )

    # Filter the events queryset with device_ids if given. Else events contain usage of all the devices
    if device_ids is not None:
        events = events.filter(device__in=device_ids)

    timedelta = (end_ts - start_ts)
    total_minutes = get_minutes_from_td(timedelta)

    devices_usage = {}

    for event in events:
        devices_usage[event.device_id] = {
            'power': event.device.power,
            'usage': event.device.power*total_minutes / 60,
            'runtime': total_minutes
        }

    for event in events:
        if (event.state_change == True):
            runtime_minutes = get_minutes_from_td(event.timestamp - start_ts)
            devices_usage[event.device_id]['runtime'] -= runtime_minutes
            devices_usage[event.device_id]['usage'] -= (
                event.device.power*runtime_minutes) / 60

        if (event.state_change == False):
            runtime_minutes = get_minutes_from_td(event.timestamp - start_ts)
            devices_usage[event.device_id]['runtime'] += runtime_minutes
            devices_usage[event.device_id]['usage'] += event.device.power * \
                runtime_minutes / 60

    for device in devices_usage.values():
        # device['runtime'] will be twice of total_minutes if it has run the whole duration. The if condition is to avoid device['runtime'] becoming 0 on modulo
        if device['runtime'] % total_minutes != 0:
            device['runtime'] %= total_minutes
            device['usage'] %= (total_minutes * device['power'] / 60)
        else:
            device['runtime'] /= 2
            device['usage'] /= 2

    devices_in_range = [device for device in devices_usage.keys()]

    devices_previously_on = list(map(
        (lambda e: e.device_id),
        filter(
            (lambda e: e.state_change == True),
            get_latest_device_states(building_id, device_ids, start_ts)
        )
    ))

    for device in list(set(devices_previously_on).difference(devices_in_range)):
        device_power = Device.objects.get(id=device).power
        devices_usage[device] = {
            'power': device_power,
            'runtime': total_minutes,
            'usage': (total_minutes * device_power) / 60
        }

    return devices_usage


def get_device_usage_timeseries(building_id, device_ids, start_ts, end_ts, frequency):
    total_minutes = get_total_minutes(frequency)

    events_timeseries = {}

    on_devices = set(list(map(
        (lambda e: e.device_id),
        filter(
            (lambda e: e.state_change == True),
            get_latest_device_states(building_id, device_ids, start_ts)
        )
    )))

    device_usage_timeseries = fetch_device_usage_timeseries(
        frequency, start_ts, end_ts, device_ids, building_id)

    device_usage_timeseries_dict = {}

    for ts, value in device_usage_timeseries:
        device_usage_timeseries_dict[ts] = value

    datetime_itr = start_ts

    while (datetime_itr < end_ts):

        events_timeseries[datetime_itr] = {
            'events': [],
            'devices_previously_on': deepcopy(on_devices)
        }

        if datetime_itr not in device_usage_timeseries_dict.keys():
            datetime_itr += timedelta(**{f'{frequency}s': 1})
            continue

        value = device_usage_timeseries_dict[datetime_itr]

        if (value is None):
            datetime_itr += timedelta(**{f'{frequency}s': 1})
            continue

        events = value.split(',')

        for event in events:
            values = event.split('|')
            device_id = int(values[0])
            state_change = values[1] == 'true'
            ts = datetime.strptime(values[2], '%Y-%m-%d %H:%M:%S.%f+00')

            events_timeseries[datetime_itr]['events'].append({
                'device_id': device_id,
                'power': Device.objects.get(id=device_id).power,
                'state_change': state_change,
                'timestamp': ts
            })

            if values[1] == 'true':
                on_devices.add(device_id)

            elif device_id in on_devices:
                on_devices.remove(device_id)

        datetime_itr += timedelta(**{f'{frequency}s': 1})

    usage_timeseries = {}
    datetime_itr = start_ts

    while (datetime_itr < end_ts):
        value = events_timeseries[datetime_itr]
        devices_usage = {}

        for event in value['events']:
            devices_usage[event['device_id']] = {
                'power': event['power'],
                'usage': (total_minutes*event['power'] / 60),
                'runtime': total_minutes
            }

        for event in value['events']:
            if (event['state_change'] == True):
                runtime_minutes = get_minutes_from_td(
                    event['timestamp'].replace(tzinfo=pytz.UTC) - datetime_itr)
                devices_usage[event['device_id']]['runtime'] -= runtime_minutes
                devices_usage[event['device_id']]['usage'] -= (
                    event['power']*runtime_minutes) / 60

            if (event['state_change'] == False):
                runtime_minutes = get_minutes_from_td(
                    event['timestamp'].replace(tzinfo=pytz.UTC) - datetime_itr)
                devices_usage[event['device_id']]['runtime'] += runtime_minutes
                devices_usage[event['device_id']]['usage'] += event['power'] * \
                    runtime_minutes / 60

        for device in devices_usage.values():
            # device['runtime'] will be twice of total_minutes if it has run the whole duration. The if condition is to avoid device['runtime'] becoming 0 on modulo
            if device['runtime'] % total_minutes != 0:
                device['runtime'] %= total_minutes
                device['usage'] %= (total_minutes * device['power'] / 60)
            else:
                device['runtime'] /= 2
                device['usage'] /= 2

        devices_in_range = [device for device in devices_usage.keys()]

        if datetime_itr + timedelta(**{f'{frequency}s': 1}) > end_ts:
            total_minutes_temp = get_minutes_from_td(end_ts - datetime_itr)
        else:
            total_minutes_temp = total_minutes

        for device in list(value['devices_previously_on'].difference(devices_in_range)):
            device_power = Device.objects.get(id=device).power
            devices_usage[device] = {
                'power': device_power,
                'runtime': total_minutes_temp,
                'usage': (total_minutes_temp * device_power) / 60
            }

        usage_timeseries[datetime_itr] = {
            'usage': 0,
            'runtime': 0
        }

        for device_id, usage in devices_usage.items():
            usage_timeseries[datetime_itr]['usage'] += usage['usage']
            usage_timeseries[datetime_itr]['runtime'] += usage['runtime']

        datetime_itr += timedelta(**{f'{frequency}s': 1})

    usage_timeseries_list = []

    for ts, value in usage_timeseries.items():
        usage_timeseries_list.append({
            'timestamp': ts,
            'usage': value['usage'],
            'runtime': value['runtime']
        })

    return usage_timeseries_list


def get_rooms_usage(building_id, room_ids, start_ts, end_ts):

    rooms_usage = {}

    for room_id in room_ids:

        rooms_usage[room_id] = {
            'usage': 0,
            'runtime': 0
        }

        device_ids = Device.objects.filter(
            room_id=room_id).values_list('id', flat=True)

        if not device_ids:
            continue

        devices_usage = get_devices_usage(
            building_id=building_id, device_ids=device_ids, start_ts=start_ts, end_ts=end_ts)

        for device_id, value in devices_usage.items():
            rooms_usage[room_id]['usage'] += value['usage']
            rooms_usage[room_id]['runtime'] += value['runtime']

    return rooms_usage
