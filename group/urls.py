from django.urls import path
from . import views

urlpatterns = [
    # ... 你已有的路由
    path("name/<str:group_name>/", views.get_group_by_name_view, name="get_group_by_name_view"),
    path("showlog/delete/<str:group_name>/<str:schedule_id>/", views.delete_showlog_inupdate, name="delete_showlog_inupdate"),
]