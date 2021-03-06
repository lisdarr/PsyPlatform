import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from database.views import *
import datetime


def record(request):
    if request.method == 'GET':
        name = request.GET.get('name', '')
        begin_date = request.GET.get('begin_date', '')
        end_date = request.GET.get('end_date', '')
        if begin_date == '':
            begin_date = datetime.datetime.strptime('2018-01-01', '%Y-%m-%d')
        else:
            begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
        if end_date == '':
            end_date = datetime.datetime.now()
        else:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') \
                       + datetime.timedelta(hours=23, minutes=59, seconds=59)

        data, err = getRecordAdmin(name, begin_date, end_date)

        if err != '':
            msg = err
        else:
            msg = 'Success!'

        res = {
            'list': data['list'],
            'total': data['total'],
            'status': 200,
            'msg': msg
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


def info(request):
    if request.method == 'GET':
        dict_data = request.GET
        name = dict_data.get('name', '')

        data = getUserAdmin(name)

        msg = {
            'list': data,
            'total': len(data),
            'msg': 'Success',
            'status': 200
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


def ban(request):
    if request.method == 'POST':
        name = request.POST.get("name")

        err = banVisitor(name)

        if err != '':
            res = {
                'msg': err,
                'status': 500
            }

            return HttpResponse(json.dumps(res, ensure_ascii=False), status=500)

        res = {
            'msg': "Success!",
            "status": 200
        }

        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


def add(request):
    if request.method == 'POST':
        print(request.POST)
        form = {
            "uuid": request.POST.get("uuid"),
            "evaluate": request.POST.get("evaluate"),
            "con_id": request.POST.get("con_id"),
            "evalution": request.POST.get("evalution")
        }

        addTalkingRecord(form)

        res = {
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


def historyConversation(request):
    if request.method == "GET":
        token = request.COOKIES.get('token')

        historyConversation, err = getHistoryConversation(token)
        if err != '':
            msg = err
            status = 500
        else:
            msg = "Success!"
            status = 200

        res = {
            "msg": msg,
            "status": status,
            "historyConversation": historyConversation
        }

        return HttpResponse(json.dumps(res, ensure_ascii=False), status=status)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)
