from datetime import datetime
from .models import Group, Showlog

class CityService:
    @staticmethod
    def get_or_create_group(group_name: str) -> Group:
        """检查团体是否存在，不存在则创建"""
        if not group_name:
            return
        try:
            if not Group.objects(name=group_name).first():
                Group(
                    name=group_name,
                    created_at=int(datetime.utcnow().timestamp() * 1000)
                ).save()
        except Exception as e:
            print(f"[ensure_group_exists] Error: {e}")

    @staticmethod
    def list_groups():
        return Group.objects.all()
    
    @staticmethod
    def delete_group(group_id: str, schedule_id: str) -> bool:
        """删除团体"""
        try:
            group = Group.objects(id=group_id).first()
            if group:
                group.delete()
                return True
            else:
                return False
        except Exception as e:
            print(f"[delete_group] Error: {e}")
            return False
    
    @staticmethod
    def create_showlog(data) -> bool:
        """检查演出记录是否存在，不存在则创建"""
        required_fields = ["group_id", "schedule_id", "date", "location", "title"]
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"缺少必填字段 {field}")  # 建议直接报错，而不是悄悄 return

        try:
            # 先检查是否存在
            exists = Showlog.objects(
                group_id=data["group_id"],
                schedule_id=data["schedule_id"]
            ).first()

            if exists:
                return False  # 已存在，不创建

            # 不存在才创建
            showlog = Showlog(
                group_id=data["group_id"],
                schedule_id=data["schedule_id"],
                date=datetime.strptime(data["date"], "%Y-%m-%d"),
                title=data["title"],
                location=data.get("location", ""),
            )
            showlog.save()
            return True  # 创建成功

        except Exception as e:
            print(f"[create_showlog] Error: {e}")
            return False