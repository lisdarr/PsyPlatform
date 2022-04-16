import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from database.views import *
import datetime


def details(request):
    if request.method == "GET":
        id = request.GET.get("id", '')

        content, err = consultantEdit(id)
        if err != '':
            msg = err
            status = 500
        else:
            msg = "Success!"
            status = 200

        res = {
            "content": content,
            "msg": msg,
            "status": status
        }

        return HttpResponse(json.dumps(res, ensure_ascii=False), status=status)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


