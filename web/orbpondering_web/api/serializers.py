"""DRF serializers for API input/output."""

from rest_framework import serializers


class ReadingRequestSerializer(serializers.Serializer):
    date = serializers.DateField(required=False)
    lat = serializers.FloatField(default=0.0)
    lon = serializers.FloatField(default=0.0)
    house_system = serializers.ChoiceField(
        choices=["whole_sign", "equal", "porphyry", "placidus"],
        default="whole_sign",
    )
    spread = serializers.ChoiceField(
        choices=["daily", "three_card", "celtic_cross"],
        default="daily",
    )
    reversed = serializers.BooleanField(default=False)


class NatalReadingRequestSerializer(ReadingRequestSerializer):
    birth_date = serializers.DateField(required=True)
    birth_time = serializers.CharField(required=False, allow_blank=True)
    birth_lat = serializers.FloatField(default=0.0)
    birth_lon = serializers.FloatField(default=0.0)
    birth_tz = serializers.CharField(required=False, allow_blank=True)
