from django.dispatch import Signal, receiver
from controlr.events.models import Event
from controlr.buildings.models import Building

event_signal = Signal()


@receiver(event_signal)
def event_signal_handler(sender, state_change=None, **kwargs):
    type = kwargs['type']
    description = kwargs['description']
    timestamp = kwargs['timestamp']
    device_id = kwargs['device_id']
    building_id = kwargs['building_id']

    Event.objects.create(
        type=type,
        state_change=state_change,
        description=description,
        timestamp=timestamp,
        device_id=device_id,
        building_id=building_id
    )
