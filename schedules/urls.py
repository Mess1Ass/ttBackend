from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_schedules),
    path("create/", views.create_schedule),
    path("<str:scheId>/", views.get_schedule),
    path("update/<str:scheId>/", views.update_schedule),
    path("delete/<str:scheId>/", views.delete_schedule),
]
