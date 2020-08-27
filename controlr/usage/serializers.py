from rest_framework import serializers


class DeviceUsageTotalSerializer(serializers.Serializer):
    total_usage = serializers.FloatField(min_value=0)
    total_runtime = serializers.DurationField(min_value=0)


class DeviceUsageTimeseriesSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    usage = serializers.FloatField()
    runtime = serializers.IntegerField()
