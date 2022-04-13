import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from database.views import *
from datetime import datetime


def register(request):
    if (request.POST):
        user = request.POST['user_info']
        err = registUser(user)

        if err is not None:
            return HttpResponse(err, status=400)
        msg = 'Register success'
        return HttpResponseRedirect('/user/login/', msg, status=200)
    else:
        err = 'No Post request'
        return HttpResponse(err, status=400)


def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        token = checkUser(name, password)
        if token == 0:
            msg = {
                'msg': "用户不存在",
                'name': name,
                'password': password,
                'status': 400
            }
            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=400)
        elif token == -1:
            msg = {
                'msg': "密码错误",
                'name': name,
                'password': password,
                'status': 400
            }
            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=400)
        msg = {
            'msg': "登录成功",
            'name': name,
            'password': password,
            'token': token,
            'status': 200
        }
        response = HttpResponse(json.dumps(msg), status=200)
        response.set_cookie('token', token, max_age=900000)
        return response


def logout(request):
    if request.method == 'POST':
        msg = {
            'msg': 'Success!',
            'status': 200
        }
        response = HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
        response.delete_cookie('token')
        return response
    else:
        return HttpResponse(status=400)


def loginInfo(request):
    if request.method == 'GET':
        token = request.COOKIES.get('token')
        data, err = getLoginInfo(token)

        if err != '':
            msg = {
                'name': '',
                'avator': '',
                'role': '',
                'id': '',
                'msg': err
            }
            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)

        else:
            msg = {
                'name': data['name'],
                'avator': data['avator'],
                'role': data['role'],
                'id': data['id'],
                'msg': 'Success!',
                'status': 200
            }
            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        msg = {
            'name': '',
            'avator': '',
            'role': '',
            'id': '',
            'msg': 'Request Method error!',
            'status': 400
        }
        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=400)


def dashboardAdmin(request):
    if request.method == 'GET':
        token = request.COOKIES.get('token')
        data, err = getDashboardAdmin(token)

        if err != '':
            msg = {
                'status': 500,
                'msg': err
            }
            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)

        msg = {
            'status': 200,
            'msg': 'Success!',
            'consultList': data['consultList'],
            'monitorList': data['monitorList'],
            'consultNum': data['consultNum'],
            'chatNum': data['chatNum'],
            'consultTodayNum': data['consultTodayNum'],
            'consultTodayTime': data['consultTodayTime'],
            'myChartData': data['myChartData'],
            'weekChartData': data['weekChartData'],
            'sumList': data['sumList'],
            'rateList': data['rateList']
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)

    else:
        msg = {
            'status': 400,
            'msg': 'Request Method error!',
        }
        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=400)


def scheduleInfo(request):
    if request.method == 'GET':
        event = getScheduleEvent()
        consultantList = getConsultantList()
        monitorList = getDirectorList()

        res = {
            'event': event,
            'consultantList': consultantList,
            'monitorList': monitorList,
            'status': 200,
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)

    else:
        msg = {
            'status': 400,
            'msg': 'Request Method error!',
        }
    return HttpResponse(json.dumps(msg, ensure_ascii=False), status=400)


def scheduleQuery(request):
    if request.method == 'GET':
        dateStr = request.GET.get('dateStr', '')
        if dateStr == '':
            date = datetime.now()
        else:
            date = datetime.strptime(dateStr, "%Y-%m-%d")
        form, err = getScheduleQuery(date)

        if err != '':
            msg = err
        else:
            msg = 'Success!'

        res = {
            'form': form,
            'msg': msg,
            'status': 200
        }

        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)

    else:
        msg = {
            'status': 400,
            'msg': 'Request Method error!',
        }
    return HttpResponse(json.dumps(msg, ensure_ascii=False), status=400)


def addSchedule(request):
    if request.method == 'POST':
        addForm = {
            'consultantId': request.POST.get('consultantId'),
            'monitorId': request.POST.get('monitorId'),
            'dateValue': request.POST.get('dateValue')
        }

        msg = addConsultantShcedule(addForm)

        if msg != '':
            res = {
                'msg': msg,
                'status': 500
            }
            return HttpResponse(json.dumps(res, ensure_ascii=False), status=500)

        res = {
            'msg': 'Success!',
            'status': 200
        }

        return HttpResponse(json.dumps(res, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)


