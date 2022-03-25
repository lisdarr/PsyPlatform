import random
import time

from django.shortcuts import render
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from utils import constants


def registUser(user):
    if user.role == 'visitor':
        err = registInDatabase(Visitor, user)
    elif user.role == 'consultant':
        err = registInDatabase(Consultant, user)
    elif user.role == 'director':
        err = registInDatabase(Director, user)

    return err


def registInDatabase(model, user):
    password = make_password(user.password)
    q, err = model(name=user.name, password=password)
    if err is not None:
        return err
    else:
        q.save()
        return err


def checkUser(name, password):
    user = ''
    if Visitor.objects.filter(name=name).count() != 0:
        user = Visitor.objects.get(name=name)

    if Consultant.objects.filter(name=name).count() != 0:
        user = Consultant.objects.get(name=name)
    if Director.objects.filter(name=name).count() != 0:
        user = Director.objects.get(name=name)
    if user == '':
        return 0
    if check_password(password, user.password):
        ticket = ''
        for i in range(15):
            s = 'abcdefghijklmnopqrstuvwxyz'
            ticket += random.choice(s)

        now_time = int(time.time())

        ticket = 'TK' + ticket + str(now_time)

        user.u_ticket = ticket
        user.save()

        return ticket
    else:
        return -1


def getDashboardConsultant(token):
    try:
        user_info = Consultant.objects.get(u_ticket=token)
    except:
        return '', 'Consultant err'

    try:
        today_info = ConToday.objects.get(con_id=user_info.con_id)
    except:
        return '', 'ConToday err'

    time = timezone.localtime(timezone.now()).strftime(("%Y-%m-%d %H:%M:%S"))
    time = time.split(' ')

    data = {'name': user_info.name,
            'time': time[1],
            'date': time[0],
            'rate': user_info.av_score,
            'squareUrl': user_info.icon,
            'consultNum': user_info.totel_num,
            'consultTodayNum': today_info.today_num,
            'consultTodayTime': today_info.today_dur,
            'callNum': today_info.now_num}

    return data, ''


def getRecordConsult(token, name, begin_date, end_date):
    try:
        user_info = Consultant.objects.get(u_ticket=token)
    except:
        return '', 'Consultant err'
    try:
        id = Visitor.objects.get(name=name).vis_id
        num = VisitorConRecord.objects.filter(vis_id=id, stime__range=[begin_date, end_date]).count()
    except:
        return '', 'VisitorConRecord err'
    time = timezone.localtime(timezone.now()).strftime(("%Y-%m-%d %H:%M:%S"))
    time = time.split(' ')
    data = {'name': user_info.name,
            'time': time[1],
            'date': time[0],
            'rate': user_info.av_score,
            'squareUrl': user_info.icon,
            'consultNum': user_info.totel_num,
            'totalSize': num
            }

    return data, ''

def getDashboardDirctor(token):
    try:
        user_info = Director.objects.get(u_ticket=token)
    except:
        return '', 'Consultant err'

    try:
        today_info = ConToday.objects.get(con_id=user_info.con_id)
    except:
        return '', 'ConToday err'


def getRecordAdmin(name, begin_date, end_date):
    id = Visitor.objects.get(name=name).vis_id
    records = VisitorConRecord.objects.filter(vis_id=id, stime__range=[begin_date,end_date])

    list = []

    for record in records:
        ele = {
            'name': name,
            'time': record.duration,
            'date': record.stime.strftime(("%Y-%m-%d %H:%M:%S")),
            'rate': record.v2c_score,
            'eva': 'No Record',
            'assit': 'No Record'
        }
        list.append(ele)

    data = {
        'list': list,
        'total': records.count()
    }
    return data


def getConsultantManage(name):
    consults = Consultant.objects.filter(name=name)
    list =[]
    for consult in consults:
        mid = ConDirRecord.objects.get(con_id=consult.con_id).dir_id
        monitor = Director.objects.get(dir_id=mid).name
        sches = ConSchedule.objects.filter(con_id=consult.con_id)
        weekday = ''
        for sche in sches:
            weekday += sche.weekday

        data = {
            'name': name,
            'monitor': monitor,
            'sum': consult.totel_num,
            'time': consult.totel_dur,
            'rate': consult.av_score,
            'weekday': weekday
        }
        list.append(data)

    return list

def getMonitorAdmin(name):
    directors = Director.objects.filter(name=name)
    list = []

    for director in directors:
        consultants = ConDirRecord.objects.filter(dir_id=director.dir_id)
        consol = ''
        for consultant in consultants:
            id = consultant.con_id
            name = Consultant.objects.get(con_id=id).name
            consol += name
        sches = DirSchedule.objects.filter(dir_id=director.dir_id)
        weekday = ''
        for sche in sches:
            weekday += sche.weekday
        sum = director.qualnum
        time = director.duration

        data = {
            'name': name,
            'consultant': consol,
            'sum': sum,
            'time': time,
            'schedule': weekday
        }
        list.append(data)

    return list


def getUserAdmin(name):
    users = Visitor.objects.filter(name=name, type=constants.Visitor)
    list = []
    for user in users:
        data = {
            'name': user.name,
            'gender': 'No Record',
            'username': user.name,
            'phonenumber': user.tele,
            'contact': user.emer_name,
            'contactnumber': user.emer_tele,
            'date': 'No Record',
            'state': constants.state[user.ban]
        }

        list.append(data)

    return list