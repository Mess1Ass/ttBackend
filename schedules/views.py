from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScheduleSerializer
from .services import ScheduleService


@api_view(["POST"])
def create_schedule(request):
    print(request.data)
    """新建演出时间表"""
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        schedule = ScheduleService.create_schedule(serializer.validated_data)
        return Response(ScheduleSerializer(schedule).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_schedules(request):
    """列出演出时间表"""
    schedules = ScheduleService.list_schedules()
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_schedule(request, scheId):
    """获取单个时间表"""
    schedule = ScheduleService.get_schedule(scheId)
    if not schedule:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(ScheduleSerializer(schedule).data)


@api_view(["PUT", "PATCH"])
def update_schedule(request, scheId):
    """更新时间表"""
    schedule = ScheduleService.get_schedule(scheId)
    if not schedule:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ScheduleSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        updated = ScheduleService.update_schedule(scheId, serializer.validated_data)
        return Response(ScheduleSerializer(updated).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_schedule(request, scheId):
    """删除时间表"""
    deleted = ScheduleService.delete_schedule(scheId)
    if not deleted:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)
