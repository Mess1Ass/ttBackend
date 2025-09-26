from datetime import datetime
from .models import City

class CityService:
    @staticmethod
    def get_or_create_city(city_name: str) -> City:
        """检查城市是否存在，不存在则创建"""
        if not city_name:
            return
        try:
            if not City.objects(name=city_name).first():
                City(
                    name=city_name,
                    created_at=int(datetime.utcnow().timestamp() * 1000)
                ).save()
        except Exception as e:
            print(f"[ensure_city_exists] Error: {e}")

    @staticmethod
    def list_cities():
        return City.objects.all()
