from rest_framework import serializers

class GroupSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    mates = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    location = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.IntegerField(read_only=True)


class ShowlogSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    group_id = serializers.CharField()
    schedule_id = serializers.CharField()
    title = serializers.CharField()
    date = serializers.CharField()
    location = serializers.CharField()
    created_at = serializers.IntegerField(read_only=True)