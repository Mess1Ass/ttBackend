from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_schedules),
    path("create/", views.create_schedule),
    path("month/", views.get_schedules_by_month, name="get_schedules_by_month"),
    path("<str:scheId>/", views.get_schedule),
    path("update/<str:scheId>/", views.update_schedule),
    path("delete/<str:scheId>/", views.delete_schedule),
    path("<str:scheId>/image/<str:filename>", views.get_schedule_image),
    
]
