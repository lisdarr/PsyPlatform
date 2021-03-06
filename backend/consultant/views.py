import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from database.views import *
import datetime


def dashboard(request):
    if request.method == 'GET':
        token = request.COOKIES.get('token')
        data, err = getDashboardConsultant(token)
        if err != '':
            msg = {'status': 500,
                   'data': '',
                   'msg': err}

            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)

        msg = {
            'tableData': data['tableData'],
            'squareUrl': data['squareUrl'],
            'value': data['rate'],
            'consultNum': data['consultNum'],
            'consultTodayNum': data['consultTodayNum'],
            'consultTodayTime': data['consultTodayTime'],
            'callNum': data['callNum'],
            'calendarData': data['calendar'],
            'status': 200,
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)

    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


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
        data, err = getRecordConsult(name, begin_date, end_date)

        if err == '':
            err = 'Success'

        msg = {
            'tableData': data,
            'totalSize': len(data),
            'status': 200,
            'msg': err
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
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

        data, monitorList, err = getConsultantManage(name)
        if err != '':
            msg = err
        else:
            msg = "Success!"
        res = {
            'monitorList': monitorList,
            'list': data,
            'total': len(data),
            'msg': msg,
            'status': 200
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
        form = {
            'name': request.POST.get("name", ''),
            'gender': request.POST.get("gender", ''),
            'age': request.POST.get("age", ''),
            'idNumber': request.POST.get("idNumber", ''),
            'phone': request.POST.get("phone", ''),
            'monitorId': request.POST.get("monitorId", ''),
            'userName': request.POST.get("userName", ''),
            'pwd': request.POST.get("pwd", ''),
            'company': request.POST.get("company", ''),
            'rank': request.POST.get("rank", ''),
            'email': request.POST.get("email", '')
        }
        err = addConsultantItem(form)
        if err != '':
            msg = err
            status = 500
        else:
            msg = "Success!"
            status = 200
        res = {
            'msg': msg,
            'status': status
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=status)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


def edit(request):
    if request.method == 'POST':
        editForm = {
            'name': request.POST.get("name"),
            'monitor': request.POST.get("monitor"),
            'id': request.POST.get("id"),
            'schedule': request.POST.get("schedule")
        }
        err1, err2 = editConsultantItem(editForm)

        if err2 != '':
            msg = {
                "msg": err1 + err2,
                "status": 500
            }
            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)
        else:
            msg = {
                "msg": err1 + err2,
                "status": 200
            }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        res = {
            "msg": "Wrong request method",
            "status": 400
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=400)


def onlineConsultants(request):
    if request.method == "GET":
        token = request.COOKIES.get('token')

        consultList = getAllOnlineConsultant(token)

        res = {
            "consultList": consultList,
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
