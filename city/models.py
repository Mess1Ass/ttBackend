from django.db import models
import mongoengine as me
from datetime import datetime

# Create your models here.


class City(me.Document):
    name = me.StringField(required=True, unique=True)  # 城市名唯一
    created_at = me.IntField(default=lambda: int(datetime.utcnow().timestamp() * 1000))

    meta = {
        'collection': 'Cities'  # MongoDB 里的集合名
    }
