from rest_framework import serializers


class DeviceUsageTotalSerializer(serializers.Serializer):
    total_usage = serializers.FloatField(min_value=0)
    total_runtime = seriazers.DurationField(min_value=0)
