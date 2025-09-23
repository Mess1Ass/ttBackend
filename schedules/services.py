from .models import Schedule, TimetableItem, SpecialEventItem
from datetime import datetime


class ScheduleService:
    """封装对 Schedule 的增删改查逻辑"""

    @staticmethod
    def create_schedule(data: dict) -> Schedule:
        schedule = Schedule(**data)
        schedule.created_at = int(datetime.utcnow().timestamp() * 1000)
        schedule.updated_at = int(datetime.utcnow().timestamp() * 1000)
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
    def update_schedule(schedule_id: str, data: dict):
        schedule = ScheduleService.get_schedule(schedule_id)
        if not schedule:
            return None

        # 处理 timetable
        if "timetable" in data:
            timetable_data = data.pop("timetable", [])
            schedule.timetable = [TimetableItem(**item) for item in timetable_data]

        # 处理 special_events
        if "special_events" in data:
            special_events_data = data.pop("special_events", [])
            schedule.special_events = [SpecialEventItem(**item) for item in special_events_data]

        # 处理普通字段
        for key, value in data.items():
            setattr(schedule, key, value)

        # 更新时间戳（毫秒）
        schedule.updated_at = int(datetime.utcnow().timestamp() * 1000)
        schedule.save()
        return schedule

    @staticmethod
    def delete_schedule(schedule_id: str) -> bool:
        schedule = ScheduleService.get_schedule(schedule_id)
        if not schedule:
            return False
        schedule.delete()
        return True
