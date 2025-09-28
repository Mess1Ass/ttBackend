from .models import Schedule, ScheduleImage, TimetableItem
from datetime import datetime


class ScheduleService:
    """封装对 Schedule 的增删改查逻辑"""

    @staticmethod
    def create_schedule(data, images):
        """
        data 结构示例:
        {
            "city": "上海",
            "date": "2025-09-23",
            "title": "测试公演",
            "groups": ["Team SII", "Team NII"],
            "images": [<InMemoryUploadedFile>, <InMemoryUploadedFile>]
        }
        """
        image_docs = []
        for img in images:
            image_docs.append(ScheduleImage(
                filename=img.name,
                content_type=img.content_type,
                data=img.read()
            ))

        schedule = Schedule(
            city=data.get("city"),
            date=data["date"],   # 不用 datetime.strptime
            title=data.get("title"),
            location=data.get("location", ""),
            groups=data.get("groups", []),
            imgs=image_docs
        )
        schedule.save()
        return schedule

    @staticmethod
    def get_schedule(schedule_id: str):
        try:
            return Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return None

    @staticmethod
    def list_schedules():
        return Schedule.objects.all()
    
    @staticmethod
    def get_schedules_by_month(year_month: str):
        """
        year_month: "2025-09"
        """
        # 生成起止范围
        start_date = f"{year_month}-01"
        # 注意月份天数，这里偷懒给个31即可，MongoDB字符串对比能自动处理（比如不会有2025-09-32）
        end_date = f"{year_month}-31"

        schedules = Schedule.objects(
            date__gte=start_date,
            date__lte=end_date
        )
        return schedules

    @staticmethod
    def update_schedule(schedule, validated_data, images):
        schedule.city = validated_data.get("city", schedule.city)
        schedule.date = validated_data.get("date", schedule.date)
        schedule.title = validated_data.get("title", schedule.title)
        schedule.groups = validated_data.get("groups", schedule.groups)
        schedule.location = validated_data.get("location", schedule.location)
        schedule.imgs = validated_data.get("imgs", schedule.imgs)

        if images:
            for img in images:
                schedule.imgs.append(ScheduleImage(
                    filename=img.name,
                    content_type=img.content_type,
                    data=img.read()
                ))
        schedule.save()
        return schedule

    @staticmethod
    def delete_schedule(schedule_id: str) -> bool:
        schedule = ScheduleService.get_schedule(schedule_id)
        if not schedule:
            return False
        schedule.delete()
        return True
    
    @staticmethod
    def delete_imgs(schedule_id: str, img_name: str) -> bool:
        schedule = ScheduleService.get_schedule(schedule_id)
        if not schedule:
            return False

        # 过滤掉要删除的图片
        new_imgs = [img for img in schedule.imgs if img.filename != img_name]

        # 如果没有变化，说明图片不存在
        if len(new_imgs) == len(schedule.imgs):
            return False

        schedule.imgs = new_imgs
        schedule.save()
        return True
