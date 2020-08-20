from datetime import datetime, timedelta
from controlr.devices.models import DeviceState
from ..apps import timer_schedule
from django.utils import timezone
from ..models import Timer


def switch_device_state(timer_id, device_id, state_change):
    print(device_id)
    DeviceState.objects.filter(device_id=device_id).update(state=state_change)
    timer_id = str(timer_id)

    if timer_schedule.get_job(timer_id):
        Timer.objects.get(id=timer_id).delete()


def add_timer(timer_id, device_id, state_change, time_delta):
    return timer_schedule.add_job(
        switch_device_state,
        'date',
        run_date=timezone.now() + time_delta,
        args=[timer_id, device_id, state_change],
        id=str(timer_id)
    )


def remove_timer(timer_id):
    timer_id = str(timer_id)
    if (timer_schedule.get_job(timer_id)):
        timer_schedule.remove_job(timer_id)
