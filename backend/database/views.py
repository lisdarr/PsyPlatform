import random
import time

from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from utils import constants


def registUser(user):
    err = ''
    if user.role == 'visitor':
        err = registInDatabase(Visitor, user)
    elif user.role == 'consultant':
        err = registInDatabase(Consultant, user)
    elif user.role == 'director':
        err = registInDatabase(Director, user)

    return err


def registInDatabase(model, user):
    password = make_password(user.password)
    q, err = model(username=user.username, password=password)
    if err is not None:
        return err
    else:
        q.save()
        return err


def checkUser(username, password):
    user = ''
    if Visitor.objects.filter(name=username).count() != 0:
        user = Visitor.objects.get(name=username)
    if Consultant.objects.filter(username=username).count() != 0:
        user = Consultant.objects.get(username=username)
    if Director.objects.filter(username=username).count() != 0:
        user = Director.objects.get(username=username)
    if user == '':
        return 0
    print(make_password(password))
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

    data = {'name': user_info.username,
            'time': time[1],
            'date': time[0],
            'rate': user_info.av_score,
            'squareUrl': user_info.icon,
            'consultNum': user_info.totel_num,
            'consultTodayNum': today_info.today_num,
            'consultTodayTime': today_info.today_dur,
            'callNum': today_info.now_num}

    return data, ''


def getRecordConsult(username, begin_date, end_date):
    try:
        visitors = Visitor.objects.filter(name=username)
    except:
        return '', 'No such Visitor'

    list = []
    for visitor in visitors:
        try:
            records = VisitorConRecord.objects.filter(vis_id=visitor.vis_id, stime__range=[begin_date, end_date])
        except:
            return [], 'No record'
        for record in records:
            ele = {
                'name': username,
                'time': record.duration,
                'date': record.stime.strftime(("%Y-%m-%d %H:%M:%S")),
                'rate': record.v2c_score,
                'comment': record.v2c_comm
            }
            list.append(ele)

    return list, ''


def getDashboardDirctor(token):
    try:
        user_info = Director.objects.get(u_ticket=token)
    except:
        return [], 'Director No Data'

    try:
        consults = Consultant.objects.filter(dir_id=user_info.dir_id)
    except:
        return [], 'No consultant'

    list =[]
    for consult in consults:
        try:
            today = ConToday.objects.get(con_id=consult.con_id)
            data = {
                'name': consult.username,
                'state': today.state
            }
        except:
            data = {}
        list.append(data)

    tableData =[]
    records = ConDirRecord.objects.filter(dir_id=user_info.dir_id)
    for record in records:
        consult = Consultant.objects.get(con_id=record.con_id)
        data = {
            'name': consult.username,
            'time': record.duration,
            'date': record.stime.strftime(("%Y-%m-%d %H:%M:%S")),
        }
        tableData.append(data)
    today_info = DirToday.objects.get(dir_id=user_info.dir_id)

    res = {
        'consultList': list,
        'consultNum': today_info.today_num,
        'directorName': user_info.username,
        'today_num': today_info.today_num,
        'today_time': today_info.today_dur,
        'squarUrl': user_info.icon,
        'tableData': tableData,
    }

    return res, ''


def getRecordDirctor(username, begin_date, end_date):
    try:
        consultants = Consultant.objects.filter(username=username)
    except:
        return [], 'No such consultant'
    list = []
    for consultant in consultants:
        try:
            records = ConDirRecord.objects.filter(con_id=consultant.con_id, stime__range=[begin_date, end_date])
        except:
            return [], 'No record'
        for record in records:
            ele = {
                'name': username,
                'time': record.duration,
                'date': record.stime.strftime(("%Y-%m-%d %H:%M:%S")),
            }
            list.append(ele)

    return list, ''


def getRecordAdmin(username, begin_date, end_date):
    try:
        visitors = Visitor.objects.filter(username=username)
    except:
        return '', 'Visitor: No data'

    list = []
    for visitor in visitors:
        try:
            records = VisitorConRecord.objects.filter(vis_id=visitor.vis_id, stime__range=[begin_date, end_date])
        except:
            return '', 'VisitorConRecord: No data'
        for record in records:
            ele = {
                'name': username,
                'time': record.duration,
                'date': record.stime.strftime(("%Y-%m-%d %H:%M:%S")),
                'rate': record.v2c_score,
                'eva': record.record,
                'assit': 'No Record'
            }
            list.append(ele)

    data = {
        'list': list,
        'total': len(list)
    }
    return data, ''


def getConsultantManage(username):
    try:
        consults = Consultant.objects.filter(username=username)
    except:
        return '', 'Consultant: No Data'
    list = []
    for consult in consults:
        mid = ConDirRecord.objects.get(con_id=consult.con_id).dir_id
        monitor = Director.objects.get(dir_id=mid).username
        sches = ConSchedule.objects.filter(con_id=consult.con_id)
        weekday = ''
        for sche in sches:
            weekday += sche.weekday

        data = {
            'name': username,
            'monitor': monitor,
            'sum': consult.totel_num,
            'time': consult.totel_dur,
            'rate': consult.av_score,
            'weekday': weekday
        }
        list.append(data)

    return list, ''


def getMonitorAdmin(name):
    directors = Director.objects.filter(username=name)
    list = []

    for director in directors:
        consultants = ConDirRecord.objects.filter(dir_id=director.dir_id)
        consol = ''
        for consultant in consultants:
            id = consultant.con_id
            username = Consultant.objects.get(con_id=id).username
            consol += username
        sches = DirSchedule.objects.filter(dir_id=director.dir_id)
        weekday = ''
        for sche in sches:
            weekday += sche.weekday
        sum = director.qualnum
        time = director.duration

        data = {
            'name': username,
            'consultant': consol,
            'sum': sum,
            'time': time,
            'schedule': weekday
        }
        list.append(data)

    return list


def getUserAdmin(username):
    users = Visitor.objects.filter(name=username, type=constants.Visitor)
    list = []
    for user in users:
        data = {
            'name': user.username,
            'gender': 'No Record',
            'username': user.username,
            'phonenumber': user.tele,
            'contact': user.emer_name,
            'contactnumber': user.emer_tele,
            'date': 'No Record',
            'state': constants.state[user.ban]
        }

        list.append(data)

    return list


def getLoginInfo(token):
    user = ''
    role = ''
    id = ''
    name = ''
    if Visitor.objects.filter(u_ticket=token).count() != 0:
        user = Visitor.objects.get(u_ticket=token)
        if user.type == 'admin':
            role = 'Admin'
        else:
            role = 'Visitor'
        id = user.vis_id
        name = user.name
    if Consultant.objects.filter(u_ticket=token).count() != 0:
        user = Consultant.objects.get(u_ticket=token)
        role = 'Consultant'
        id = user.con_id
        name = user.username
    if Director.objects.filter(u_ticket=token).count() != 0:
        user = Director.objects.get(u_ticket=token)
        role = 'Director'
        id = user.dir_id
        name = user.username

    if user == '':
        err = 'User is not registered'
        data = {
            'name': '',
            'avator': '',
            'role': '',
            'id': ''
        }
        return data, err

    avator = user.icon

    data = {
        'name': name,
        'avator': avator,
        'role': role,
        'id': id
    }

    return data, ''

