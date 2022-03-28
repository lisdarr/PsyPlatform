import json
from django.views.decorators.http import require_http_methods
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
    else:
        err = 'No Post request'
        return HttpResponse(err, status=400)

    return HttpResponseRedirect('/user/login/', msg, status=200)

def login(request):
    if request.method=='POST':
        name = request.POST['username']
        print(name)
        password = request.POST['password']
        print(password)
        ticket = checkUser(name, password)
        if ticket == 0:
            msg = {
                'msg': "用户不存在",
                'name': name,
                'password': password,
                'status': 400
            }
            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=400)
        elif ticket == -1:
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
            'token': ticket,
            'status': 200
        }
        response = HttpResponse(json.dumps(msg), status=200)
        response.set_cookie('token', ticket, max_age=900000)
        print(response)
        return response


def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/user/login/')
        response.delete_cookie('ticket')
        return response


def dashboardConsultant(request):
    if request.method == 'GET':
        token = request.COOKIES.get('ticket')

        data, err = getDashboardConsultant(token)

        if err != '':
            msg = {'status': 500,
                   'data': '',
                   'msg': err}

            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)
        tableData = {'name': data['name'],
                     'time': data['time'],
                     'date': data['date'],
                     'rate': data['rate'],
                     'comment': '404 Not Found'}

        msg = {'tableData': tableData,
               'squareUrl': data['squareUrl'],
               'value': data['rate'],
               'consultNum': data['consultNum'],
               'consultTodayNum': data['consultTodayNum'],
               'consultTodayTime': data['consultTodayTime'],
               'callNum': data['callNum']}

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)

    else:
        return HttpResponse(status=400)


def recordConsultant(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        begin_date = request.GET.get('begin_date')
        end_date = request.GET.get('end_date')
        begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        data, err = getRecordConsult(name, begin_date, end_date)

        if err != '':
            msg = {'status': 500,
                   'data': '',
                   'msg': err}

            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)

        msg = {
            'tableData': data,
            'totalSize': len(data)
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)


def dashboardDirector(request):
    if request.method == 'GET':
        token = request.COOKIES.get('ticket')

        data, err = getDashboardDirctor(token)

        if err != '':
            msg = {'status': 500,
                   'data': '',
                   'msg': err}

            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)

        return HttpResponse(json.dumps(data, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)


def recordDirector(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        begin_date = request.GET.get('begin_date')
        end_date = request.GET.get('end_date')
        begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        data, err = getRecordDirctor(name, begin_date, end_date)

        if err != '':
            msg = {'status': 500,
                   'data': '',
                   'msg': err}

            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)

        msg = {
            'tableData': data,
            'totalSize': len(data),
            'status': 200,
            'msg': 'Success'
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)


def recordAdmin(request):
    if request.method == 'GET':
        dict_data = request.GET
        name = dict_data.get('name')
        begin_date = dict_data.get('begin_date')
        end_date = dict_data.get('end_date')
        begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        data, err = getRecordAdmin(name, begin_date, end_date)

        if err != '':
            msg = {'status': 500,
                   'data': '',
                   'msg': err}

            return HttpResponse(json.dumps(msg, ensure_ascii=False), status=500)

        return HttpResponse(json.dumps(data, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)


def consultantAdmin(request):
    if request.method == 'GET':
        dict_data = request.GET
        name = dict_data.get('name')

        data = getConsultantManage(name)

        msg = {
            'list': data,
            'total': len(data),
            'msg': 'Success',
            'status': 200
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)


def monitorAdmin(request):
    if request.method == 'GET':
        dict_data = request.GET
        name = dict_data.get('name')

        data = getMonitorAdmin(name)

        msg = {
            'list': data,
            'total': len(data),
            'msg': 'Success',
            'status': 200
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)


def userAdmin(request):
    if request.method == 'GET':
        dict_data = request.GET
        name = dict_data.get('name')

        data = getUserAdmin(name)

        msg = {
            'list': data,
            'total': len(data),
            'msg': 'Success',
            'status': 200
        }

        return HttpResponse(json.dumps(msg, ensure_ascii=False), status=200)
    else:
        return HttpResponse(status=400)
