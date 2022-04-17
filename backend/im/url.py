from django.urls import path
from .views import *

urlpatterns = [
    path('details/', details),
    path('userList/', userList),
    path('director/', director),
    path('record/save/cv/', cvRecordSAVE),
    path('record/save/cd/', cdRecordSAVE),
    path('eachRecord/get/', eachRecordGET),
]
