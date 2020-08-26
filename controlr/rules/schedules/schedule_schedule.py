from datetime import datetime, timedelta
from controlr.devices.models import DeviceState
from controlr.core.scheduler import schedule_sched
from django.utils import timezone
from ..models import Timer


def add_schedule(schedule_id, device_id, state_change, days_of_week, hour, minute):
    days_of_week_str = ','.join(map(str, days_of_week))

    return schedule_sched.add_job(
        switch_device_state,
        trigger='cron',
        day_of_week=days_of_week_str,
        hour=hour,
        minute=minute,
        args=[device_id, state_change],
        id=str(schedule_id)
    )


def remove_schedule(schedule_id):
    schedule_id = str(schedule_id)
    if (schedule_sched.get_job(schedule_id)):
        schedule_sched.remove_job(schedule_id)


def switch_device_state(device_id, state_change):
    DeviceState.objects.filter(device_id=device_id).update(state=state_change)


def switch_schedule_state(schedule_id, state_change):
    if (state_change):
        schedule_sched.resume_job(str(schedule_id))
    elif not (state_change):
        schedule_sched.pause_job(str(schedule_id))
