import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from database.views import *
import datetime


def details(request):
    if request.method == "GET":
        id = request.GET.get("id")

        content = consultantEdit(id)

        res = {
            "content": content,
            "status": 200
        }

        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


