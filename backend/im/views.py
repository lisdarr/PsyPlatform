import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from database.views import *
import datetime


def details(request):
    if request.method == "GET":
        id = request.GET.get("id", '')
        type = request.GET.get("type", '')
        content, err = getDetails(id, type)
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


def userList(request):
    if request.method == 'GET':
        content = getUserList()
        res = {
            "content": content,
            "msg": "Success!",
            "status": 200
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


def director(request):
    if request.method == "GET":
        id = request.GET.get('id')
        content = askForDir(id)

        res = {
            "content": content,
            "status": 200,
            "msg": "Success!"
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


def cvRecordSAVE(request):
    if request.method == "POST":
        form = {
            "vis_name": request.POST.get("vis_name"),
            "con_name": request.POST.get("con_name"),
            "time": request.POST.get("time"),
            "date": request.POST.get("date"),
            "id": request.POST.get("id")
        }

        err = saveCVRecord(form)

        if err != "":
            msg = err
            status = 500
        else:
            msg = "Success!"
            status = 200

        res = {
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


def cdRecordSAVE(request):
    if request.method == "POST":
        form = {
            "id": request.POST.get("id"),
            "con_name": request.POST.get("con_name"),
            "dir_name": request.POST.get("dir_name"),
            "time": request.POST.get("time"),
            "date": request.POST.get("date"),
        }

        err = saveCDRecord(form)

        if err != "":
            msg = err
            status = 500
        else:
            msg = "Success!"
            status = 200

        res = {
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


def eachRecordGET(request):
    if request.method == "GET":
        id = request.GET.get("id")
        type = request.GET.get("type")
        records = getIMRecord(id, type)

        res = {
            "records": records,
            "msg": "Success!",
            "status": 200
        }

        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


def eachRecordSAVE(request):
    if request.method == "POST":
        forms = json.loads(request.POST.get("chathistory"))
        err = saveIMRecord(forms)
        if err != "":
            msg = err
            status = 500
        else:
            msg = "Success!"
            status = 200
        res = {
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


def consultList(request):
    if request.method == 'GET':
        content = getConsultList()
        res = {
            "content": content,
            "msg": "Success!",
            "status": 200
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)
