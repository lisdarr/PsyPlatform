from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    path('weChat/login/', wlogin),
    path('register/', register),
    path('info/', loginInfo),
    path('logout/', logout),
    path('dashboard/', dashboardAdmin),
    path('schedule/info/', scheduleInfo),
    path('schedule/query/', scheduleQuery),
    path('schedule/add/', addSchedule),
    path('fresh/', fresh)
]