from datetime import datetime, timedelta
from controlr.devices.models import DeviceState
from controlr.core.scheduler import timer_sched
from django.utils import timezone
from ..models import Timer


def switch_device_state(timer_id, device_id, state_change):
    DeviceState.objects.filter(device_id=device_id).update(state=state_change)
    timer_id = str(timer_id)

    if timer_sched.get_job(timer_id):
        Timer.objects.get(id=timer_id).delete()


def add_timer(timer_id, device_id, state_change, time_delta):
    print('Timer Added')
    return timer_sched.add_job(
        switch_device_state,
        'date',
        run_date=timezone.now() + time_delta,
        args=[timer_id, device_id, state_change == 'true'],
        id=str(timer_id)
    )


def remove_timer(timer_id):
    timer_id = str(timer_id)
    if (timer_sched.get_job(timer_id)):
        timer_sched.remove_job(timer_id)
