import mongoengine as me
import time
from datetime import datetime

# 时间表的子项
class TimetableItem(me.EmbeddedDocument):
    group = me.StringField()       # 演出团体
    start_time = me.StringField()               # 开始时间（字符串形式，前端可灵活传）
    end_time = me.StringField()                 # 结束时间
    bonus_time = me.StringField()
    

class ScheduleImage(me.EmbeddedDocument):
    filename = me.StringField()
    content_type = me.StringField()
    data = me.BinaryField()   # 直接存图片二进制

# 主文档：演出时间表
class Schedule(me.Document):
    location = me.StringField(required=True)    # 地点
    title = me.StringField(required=True)       # 演出标题
    date = me.StringField(required=True)        # 演出时间
    city = me.StringField()
    groups = me.ListField(me.StringField())
    imgs = me.ListField(me.EmbeddedDocumentField(ScheduleImage))

    # entry_time = me.StringField()               # 进场时间
    # start_time = me.StringField(required=True)  # 开始时间
    # timetable = me.ListField(me.EmbeddedDocumentField(TimetableItem))  # 时间表
    

    created_at = me.FloatField(default=lambda: int(time.time() * 1000))  # 秒级时间戳
    updated_at = me.FloatField(default=lambda: int(time.time() * 1000))

    meta = {'collection': 'Schedules'}  # 存储到 MongoDB 的集合名
