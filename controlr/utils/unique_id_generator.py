import shortuuid
from controlr.devices.models import Device
from controlr.settings import UNIQUE_ID_LENGTH


def generate_unique_id(length=UNIQUE_ID_LENGTH):
    device_exists = True

    while device_exists:
        unique_id = shortuuid.ShortUUID().random(length=length)
        device_exists = Device.objects.filter(unique_id=unique_id)

    return unique_id
