import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from database.views import *
import datetime


def dashboard(request):
    if request.method == 'GET':
        token = request.COOKIES.get('token')

        data, err = getDashboardDirector(token)

        if err != '':
            msg = {'status': 500,
                   'data': '',
                   'msg': err}

            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)

        msg = {
            'status': 200,
            'msg': 'Success!',
            'consultList': data['consultList'],
            'consultNum': data['consultNum'],
            'directorName': data['directorName'],
            'today_num': data['today_num'],
            'today_time': data['today_time'],
            'squarUrl': data['squarUrl'],
            'tableData': data['tableData'],
            'calendarData': data['calendarData'],
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)


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
        data, err = getRecordDirector(name, begin_date, end_date)

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
        return HttpResponse(status=400)


def info(request):
    if request.method == 'GET':
        dict_data = request.GET
        name = dict_data.get('name', '')

        data, qualList = getMonitorAdmin(name)

        msg = {
            'list': data,
            'qualList': qualList,
            'total': len(data),
            'msg': 'Success',
            'status': 200
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)


def add(request):
    if request.method == 'POST':
        form = {
            'name': request.POST.get("name"),
            'gender': request.POST.get("gender"),
            'age': request.POST.get("age"),
            'idNumber': request.POST.get("idNumber"),
            'phone': request.POST.get("phone"),
            'email': request.POST.get("email"),
            'userName': request.POST.get("userName"),
            'pwd': request.POST.get("pwd"),
            'company': request.POST.get("company"),
            'rank': request.POST.get("rank"),
            'qualId': request.POST.get("qualId"),
            'certId': request.POST.get("certId"),
        }
        addDirectorItem(form)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def edit(request):
    if request.method == 'POST':
        editForm = {
            'name': request.POST.get("name"),
            'id': request.POST.get("id"),
            'schedule': request.POST.get("schedule")
        }
        msg, err = editDirectorItem(editForm)

        if err != '':
            msg = {
                "msg": err,
                "status": 500
            }
            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)
        else:
            msg = {
                "msg": msg,
                "status": 200
            }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)
