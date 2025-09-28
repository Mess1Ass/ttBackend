from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, Http404
import threading
from .models import Schedule, ScheduleImage
from .serializers import ScheduleSerializer, ScheduleImageSerializer
from .services import ScheduleService
from city.services import CityService   # 引用 city 的服务


@api_view(["POST"])
def create_schedule(request):
    """新建演出时间表"""
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data

        imgs = request.FILES.getlist("imgs")

        # ✅ 调用 service 层
        schedule = ScheduleService.create_schedule(data, imgs)

        # 🚀 异步触发 city 检查
        city_name = data.get("city")
        if city_name:
            threading.Thread(target=CityService.get_or_create_city, args=(city_name,)).start()

        # ✅ 返回时序列化 imgs → url
        resp_data = ScheduleSerializer(schedule).data
        resp_data["imgs"] = ScheduleImageSerializer(schedule.imgs, many=True, context={"schedule": schedule}).data

        return Response(resp_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_schedules(request):
    """列出演出时间表"""
    schedules = ScheduleService.list_schedules()
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_schedules_by_month(request):
    """按月份查询演出时间表"""
    year_month = request.query_params.get("month")  # 前端传 ?month=2025-09
    if not year_month:
        return Response({"error": "缺少参数 month，例如 2025-09"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        schedules = ScheduleService.get_schedules_by_month(year_month)

        resp_data = []
        for schedule in schedules:
            s_data = ScheduleSerializer(schedule).data
            s_data["imgs"] = ScheduleImageSerializer(
                schedule.imgs,
                many=True,
                context={"schedule": schedule}
            ).data
            resp_data.append(s_data)

        return Response(resp_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
def get_schedule_image(request, scheId, filename):
    """获取某个 schedule 的指定图片"""
    schedule = ScheduleService.get_schedule(scheId)
    if not schedule:
        raise Http404("Schedule not found")

    img = next((i for i in schedule.imgs if i.filename == filename), None)
    if not img:
        raise Http404("Image not found")

    return HttpResponse(img.data, content_type=img.content_type)


@api_view(["GET"])
def get_schedule(request, scheId):
    """获取单个时间表"""
    schedule = ScheduleService.get_schedule(scheId)
    if not schedule:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(ScheduleSerializer(schedule).data)


@api_view(["PUT"])
def update_schedule(request, scheId):
    """更新时间表"""
    schedule = ScheduleService.get_schedule(scheId)
    if not schedule:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ScheduleSerializer(schedule, data=request.data, partial=True)
    if serializer.is_valid():
        # 处理图片（可选，前端如果没传，就不更新）
        images = request.FILES.getlist("imgs")
        print("imgs:", images)

        updated = ScheduleService.update_schedule(schedule, serializer.validated_data, images)

        # 🚀 异步触发 city 检查
        city_name = serializer.validated_data.get("city")
        if city_name:
            threading.Thread(target=CityService.get_or_create_city, args=(city_name,)).start()

        return Response(ScheduleSerializer(updated).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_schedule(request, scheId):
    """删除时间表"""
    deleted = ScheduleService.delete_schedule(scheId)
    if not deleted:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["DELETE"])
def delete_schedule_image(request, schedule_id: str, img_name: str):
    """
    删除指定演出时间表的图片
    URL 示例: DELETE /schedule/<schedule_id>/image/<img_name>/
    """
    success = ScheduleService.delete_imgs(schedule_id, img_name)
    if success:
        return Response({"message": "图片删除成功"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "图片不存在或演出时间表未找到"}, status=status.HTTP_404_NOT_FOUND)
