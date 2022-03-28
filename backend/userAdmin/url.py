from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('dashboard/consultant/', dashboardConsultant),
    path('dashboard/director/', dashboardDirector),
    path('record/consultant/', recordConsultant),
    path('record/director/', recordDirector),
    path('admin/record/', recordAdmin),
    path('admin/consultant', consultantAdmin),
    path('admin/monitor', monitorAdmin),
    path('admin/user', userAdmin),
    path('info/', loginInfo),
    path('logout/', logout)
]