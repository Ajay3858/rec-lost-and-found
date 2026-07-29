from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
path("profile/", views.profile, name="profile"),
    path("report/lost/", views.report_lost, name="report_lost"),
    path("report/found/", views.report_found, name="report_found"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("lost/", views.lost_items, name="lost_items"),
    path("found/", views.found_items, name="found_items"),
]