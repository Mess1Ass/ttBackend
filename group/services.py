import re
from datetime import datetime
from mongoengine.queryset.visitor import Q
from .models import Group, Showlog

class GroupService:
    @staticmethod
    def get_or_create_group(group_name: str) -> Group:
        """检查团体是否存在，不存在则创建（先严格，后模糊）"""
        if not group_name:
            return None
        try:
            # 1. 严格匹配
            group = Group.objects(name=group_name).first()

            # 2. 双向模糊匹配（只在没找到时才查）
            if not group:
                group = Group.objects(
                    Q(name__icontains=group_name) | Q(name__regex=f".*{group_name}.*")
                ).first()

            # 3. 都没有 → 创建新 group
            if not group:
                group = Group(
                    name=group_name,
                    mates=[],
                    location="",
                    created_at=int(datetime.utcnow().timestamp() * 1000)
                )
                group.save()
            return group

        except Exception as e:
            print(f"[get_or_create_group] Error: {e}")
            return None

    @staticmethod
    def list_groups():
        return Group.objects.all()
    
    @staticmethod
    def get_group_and_showlog_byname(group_name: str):
        """获取团体信息（带 showlogs，确保可 JSON 序列化）"""
        try:
            group = Group.objects(name=group_name).first()
            if not group:
                return None

            # 转成 dict
            group_dict = group.to_mongo().to_dict()

            # 转换 ObjectId 为 str
            group_dict["id"] = str(group.id)
            if "_id" in group_dict:
                group_dict["_id"] = str(group_dict["_id"])

            # showlogs
            showlogs = []
            for log in Showlog.objects(group_id=str(group.id)):
                log_dict = log.to_mongo().to_dict()
                log_dict["id"] = str(log.id)
                if "_id" in log_dict:
                    log_dict["_id"] = str(log_dict["_id"])
                showlogs.append(log_dict)

            group_dict["showlogs"] = showlogs

            return group_dict

        except Exception as e:
            print(f"[get_group_and_showlog_byname] Error: {e}")
            return None
        
    @staticmethod
    def update_group(group_id: str, data) -> bool:
        """更新团体信息"""
        group = Group.objects(id=group_id).first()
        if group:
            group.name = data.get("name", group.name)
            group.location = data.get("location", group.location)
            group.mates = data.get("mates", group.mates)
            group.save()
        return group

    
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

class ShowlogService:
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
                date=data["date"],
                title=data["title"],
                location=data.get("location", ""),
            )
            showlog.save()
            return True  # 创建成功

        except Exception as e:
            print(f"[create_showlog] Error: {e}")
            return False
        
    @staticmethod
    def get_showlog(group_id: str, schedule_id: str) -> Showlog:
        """获取演出记录"""
        try:
            showlog = Showlog.objects(
                group_id=str(group_id).strip(),
                schedule_id=str(schedule_id).strip()
            ).first()
            return showlog
        except Exception as e:
            print(f"[get_showlog] Error: {e}")

        

    @staticmethod
    def update_showlog(showlog, data) -> bool:
        """更新演出记录"""
        showlog.date = data.get("date", showlog.date)
        showlog.title = data.get("title", showlog.title)
        showlog.location = data.get("location", showlog.location)
        showlog.save()

        return showlog
    
    @staticmethod
    def delete_showlog(group_id: str, schedule_id: str) -> bool:
        """删除演出记录"""
        try:
            group_id = str(group_id).strip()
            schedule_id = str(schedule_id).strip()

            showlog = Showlog.objects(
                group_id=str(group_id).strip(),
                schedule_id=str(schedule_id).strip()
            ).first()

            if showlog:
                showlog.delete()
                return True
            else:
                return False
        except Exception as e:
            print(f"[delete_showlog] Error: {e}")
            return False

