from rest_framework import serializers


class TimetableItemSerializer(serializers.Serializer):
    group = serializers.CharField()
    start_time = serializers.CharField(required=False, allow_blank=True)
    end_time = serializers.CharField(required=False, allow_blank=True)


class SpecialEventItemSerializer(serializers.Serializer):
    group = serializers.CharField()
    start_time = serializers.CharField(required=False, allow_blank=True)
    end_time = serializers.CharField(required=False, allow_blank=True)


class ScheduleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)   # MongoDB 的 _id
    location = serializers.CharField()
    title = serializers.CharField()
    date = serializers.CharField()
    entry_time = serializers.CharField()
    start_time = serializers.CharField()
    timetable = TimetableItemSerializer(many=True)
    special_events = SpecialEventItemSerializer(many=True)
    created_at = serializers.FloatField(read_only=True)  
    updated_at = serializers.FloatField(read_only=True)
