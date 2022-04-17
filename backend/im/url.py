from django.urls import path
from .views import *

urlpatterns = [
    path('details/', details),
    path('userList/', userList)
]