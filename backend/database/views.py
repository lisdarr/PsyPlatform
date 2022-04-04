import random
import time

from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from utils import constants, convert
from django.db.models.aggregates import Sum, Count, Avg, Variance, StdDev, Max, Min


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

    try:
        conschedule = ConSchedule.objects.filter(con_id=user_info.con_id)

    except:
        return '', 'ConSchedule err'

    time = timezone.localtime(timezone.now()).strftime(("%Y-%m-%d %H:%M:%S"))
    time = time.split(' ')
    calendar = []
    for sch in conschedule:
        list = convert.get_date(sch.weekday)
        for i in list:
            calendar.append(i)

    data = {'name': user_info.username,
            'time': time[1],
            'date': time[0],
            'rate': user_info.av_score,
            'squareUrl': user_info.icon,
            'consultNum': user_info.totel_num,
            'consultTodayNum': today_info.today_num,
            'consultTodayTime': today_info.today_dur,
            'callNum': today_info.now_num,
            'calendar': calendar,
            }

    return data, ''


def getRecordConsult(username, begin_date, end_date):
    if username == '':
        visitors = Visitor.objects.all()
    else:
        try:
            visitors = Visitor.objects.filter(name=username)
        except Visitor.DoesNotExist:
            return '', 'No such Visitor'

    list = []
    for visitor in visitors:
        try:
            records = VisitorConRecord.objects.filter(vis_id=visitor.vis_id, stime__range=[begin_date, end_date])
        except VisitorConRecord.DoesNotExist:
            continue
        for record in records:
            if username == '':
                username = Visitor.objects.get(vis_id=record.vis_id).name
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
        return '', 'Director No Data'

    try:
        consults = Consultant.objects.filter(dir_id=user_info.dir_id)
    except:
        return '', 'No consultant'

    try:
        dirSchedule = DirSchedule.objects.filter(dir_id=user_info.dir_id)
    except:
        return '', 'DirSchedule err'

    list = []
    for consult in consults:
        try:
            today = ConToday.objects.get(con_id=consult.con_id)
            data = {
                'name': consult.username,
                'state': today.state
            }
            list.append(data)
        except:
            data = {}

    tableData = []
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

    calendarData = []
    for sch in dirSchedule:
        list = convert.get_date(sch.weekday)
        for i in list:
            calendarData.append(i)

    res = {
        'consultList': list,
        'consultNum': today_info.today_num,
        'directorName': user_info.username,
        'today_num': today_info.today_num,
        'today_time': today_info.today_dur,
        'squarUrl': user_info.icon,
        'tableData': tableData,
        'calendarData': calendarData,
    }

    return res, ''


def getRecordDirctor(username, begin_date, end_date):
    if username == '':
        consultants = Consultant.objects.all()
    else:
        try:
            consultants = Consultant.objects.filter(username=username)
        except Consultant.DoesNotExist:
            return [], 'No such consultant'
    list = []
    for consultant in consultants:
        try:
            records = ConDirRecord.objects.filter(con_id=consultant.con_id, stime__range=[begin_date, end_date])
        except ConDirRecord.DoesNotExist:
            continue
        for record in records:
            if username == '':
                username = Consultant.objects.get(con_id=record.con_id).username
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
    role = []
    id = ''
    name = ''
    if Visitor.objects.filter(u_ticket=token).count() != 0:
        user = Visitor.objects.get(u_ticket=token)
        if user.type == constants.Admin:
            role.append('Admin')
        else:
            role.append('Visitor')
        id = user.vis_id
        name = user.name
    if Consultant.objects.filter(u_ticket=token).count() != 0:
        user = Consultant.objects.get(u_ticket=token)
        role.append('Consultant')
        id = user.con_id
        name = user.username
    if Director.objects.filter(u_ticket=token).count() != 0:
        user = Director.objects.get(u_ticket=token)
        role.append('Director')
        id = user.dir_id
        name = user.username

    if user == '':
        err = 'User is not registered'
        data = {
            'name': '',
            'avator': '',
            'role': [],
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


def getDashboardAdmin(token):
    try:
        admin = Visitor.objects.filter(u_ticket=token)
    except:
        return '', 'User is not admin'

    if admin.count() == 0:
        return '', 'User is not admin'

    try:
        consultants = Consultant.objects.all()
    except:
        return '', 'Consultant err'

    consultantList = []
    for consultant in consultants:
        try:
            state = ConToday.objects.get(con_id=consultant.con_id).state
        except:
            state = 0
        data = {
            'name': consultant.username,
            'state': state
        }
        consultantList.append(data)

    try:
        dirctors = Director.objects.all()
    except:
        return '', 'Director err'

    directorList = []
    for dirctor in dirctors:
        try:
            state = DirToday.objects.get(dir_id=dirctor.dir_id).state
        except:
            state = 'NULL'

        data = {
            'name': dirctor.username,
            'state': state
        }

        directorList.append(data)

    consultNum = ConToday.objects.filter(state=1).count()
    chatNum = DirToday.objects.filter(state=1).count()
    consultTodayNum = ConToday.objects.aggregate(nums=Sum('today_num'))['nums']
    consultTodayTime = ConToday.objects.all().aggregate(duration=Sum('today_dur'))['duration']

    firstDay = convert.get_past_week()
    weekchartDatas = VisitorConRecord.objects.filter(stime__gte=firstDay)

    chartMap = {}
    weekChartData = []
    for chart in weekchartDatas:
        date = str(chart.stime.strftime('%m-%d'))
        num = chartMap.get(date, 0)
        chartMap[date] = num + 1
    days = convert.get_last_week()
    for day in days:
        date = str(day.strftime('%m-%d'))
        num = chartMap.get(date, 0)
        chartMap[date] = num

    for key, value in chartMap.items():
        list = [key, value]
        weekChartData.append(list)

    firstHour = convert.get_last_day()
    hourChartDatas = VisitorConRecord.objects.filter(stime__gte=firstHour)
    myChartData = []
    map = {}
    for data in hourChartDatas:
        hour = str(data.stime.strftime('%H'))
        num = map.get(hour, 0)
        map[hour] = num + 1

    hours = convert.get_last_hour()
    for h in hours:
        hour = str(h.strftime('%H'))
        num = map.get(hour, 0)
        map[hour] = num

    for key, value in map.items():
        key = key + ':00'
        list = [key, value]
        myChartData.append(list)

    consultants = Consultant.objects.all().order_by('totel_num')[:4]
    sumList = []

    for consult in consultants:
        data = {
            'photo': consult.icon,
            'name': consult.username,
            'consultNum': consult.totel_num
        }
        sumList.append(data)

    rateList = []
    consultants = Consultant.objects.all().order_by('av_score')[:4]

    for consult in consultants:
        data = {
            'photo': consult.icon,
            'name': consult.username,
            'consultNum': consult.av_score
        }

        rateList.append(data)

    res = {
        'consultList': consultantList,
        'monitorList': directorList,
        'consultNum': consultNum,
        'chatNum': chatNum,
        'consultTodayNum': consultTodayNum,
        'consultTodayTime': consultTodayTime,
        'myChartData': myChartData,
        'weekChartData': weekChartData,
        'sumList': sumList,
        'rateList': rateList,
    }

    return res, ''


# def addConsultant(form):
