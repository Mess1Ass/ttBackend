from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_schedules),
    path("create/", views.create_schedule),
    path("month/", views.get_schedules_by_month, name="get_schedules_by_month"),

    # 图片相关接口先放前面
    path("<str:schedule_id>/imageDelete/<str:img_name>/", views.delete_schedule_image, name="delete_schedule_image"),
    path("<str:scheId>/image/<str:filename>/", views.get_schedule_image),

    # schedule 相关操作
    path("<str:scheId>/", views.get_schedule),
    path("update/<str:scheId>/", views.update_schedule),
    path("delete/<str:scheId>/", views.delete_schedule),
]
