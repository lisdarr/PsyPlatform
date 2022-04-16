from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # path('dashboard/', dashboard),
    path('record/', record),
    path('info/', info),
    path('ban/', ban),
    path('weChat/add/', add),
    path('weChat/conversation/', historyConversation)
]