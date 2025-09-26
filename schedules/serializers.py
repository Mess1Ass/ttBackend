from rest_framework import serializers
import base64


class TimetableItemSerializer(serializers.Serializer):
    group = serializers.CharField()
    start_time = serializers.CharField(required=False, allow_blank=True)
    end_time = serializers.CharField(required=False, allow_blank=True)
    bonus_time = serializers.CharField(required=False, allow_blank=True)


class ScheduleImageSerializer(serializers.Serializer):
    filename = serializers.CharField()
    content_type = serializers.CharField()
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        schedule = self.context.get("schedule")
        if schedule:
            return f"/schedule/{schedule.id}/image/{obj.filename}"
        return None


class ScheduleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)   # MongoDB 的 _id
    location = serializers.CharField()
    title = serializers.CharField()
    date = serializers.CharField()
    city = serializers.CharField()
    groups = serializers.ListField(child=serializers.CharField())
    imgs = serializers.SerializerMethodField()   # 只负责返回

    def get_imgs(self, obj):
        # 把 schedule 传给子序列化器的 context
        return ScheduleImageSerializer(obj.imgs, many=True, context={"schedule": obj}).data

    # entry_time = serializers.CharField()
    # start_time = serializers.CharField()
    # timetable = TimetableItemSerializer(many=True)
    
    created_at = serializers.FloatField(read_only=True)  
    updated_at = serializers.FloatField(read_only=True)
