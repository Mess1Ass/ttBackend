from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from .services import ShowlogService, GroupService # 确保导入了 Service
from .serializers import GroupSerializer

# Create your views here.
@api_view(["GET"])
def list_groups(request):
    """获取所有团体列表"""
    groups = GroupService.list_groups()
    return Response(GroupSerializer(groups, many=True).data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_group(request, groupId):
    """更新团体信息"""
    data = request.data
    updated = GroupService.update_group(groupId, data)
    if not updated:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

    # 返回序列化后的 group
    return Response(GroupSerializer(updated).data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_showlog_inupdate(request, group_name, schedule_id):
    """删除该团体演出记录"""
    try:
        group_id = GroupService.get_group_byname(group_name).id
        deleted = ShowlogService.delete_showlog(group_id, schedule_id)
        if deleted:
            return Response({"message": "删除成功"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "未找到对应的演出记录"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
def get_group_by_name_view(request, group_name: str):
    """
    通过 group_name 获取 Group 信息
    """
    group = GroupService.get_group_and_showlog_byname(group_name)
    if not group:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(group, status=status.HTTP_200_OK)