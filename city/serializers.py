from rest_framework import serializers

class CitySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    created_at = serializers.IntegerField(read_only=True)
