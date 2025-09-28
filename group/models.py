from django.db import models
import mongoengine as me
from datetime import datetime

# Create your models here.
class Group(me.Document):
    name = me.StringField(required=True, unique=True)  # 组合名唯一
    mates = me.ListField(me.StringField())
    location = me.StringField()

    

    meta = {
        'collection': 'Groups'  # MongoDB 里的集合名
    }


class Showlog(me.Document):
    group_id = me.StringField(required=True)  # 外键组合id
    schedule_id = me.StringField(required=True)  # 外键日程表id
    title = me.StringField(required=True)
    date = me.StringField(required=True)
    location = me.StringField(required=True)
    # start_time = me.StringField()
    # end_time = me.StringField()
    # bonus_time = me.StringField()
    created_at = me.IntField(default=lambda: int(datetime.utcnow().timestamp() * 1000))

    meta = {
        'collection': 'Showlogs'  # MongoDB 里的集合名
    }    