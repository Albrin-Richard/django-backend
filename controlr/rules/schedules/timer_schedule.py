from datetime import datetime, timedelta
from controlr.devices.models import DeviceState
from controlr.core.scheduler import timer_sched
from django.utils import timezone
from ..models import Timer


def switch_device_state(timer_id, device_id, state_change):
    DeviceState.objects.filter(device_id=device_id).update(state=state_change)
    for i in DeviceState.objects.filter(device_id=device_id):
        print(i)

    timer_id = str(timer_id)

    if timer_sched.get_job(timer_id):
        Timer.objects.get(id=timer_id).delete()


def add_timer(timer_id, device_id, state_change, trigger_time):
    timer_sched.add_job(
        switch_device_state,
        'date',
        run_date=trigger_time,
        args=[timer_id, device_id, state_change],
        id=str(timer_id)
    )
    timer_sched.print_jobs()


def remove_timer(timer_id):
    timer_id = str(timer_id)
    if (timer_sched.get_job(timer_id)):
        timer_sched.remove_job(timer_id)
