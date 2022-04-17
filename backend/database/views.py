import random
import time

from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from utils import constants, convert
from django.db.models.aggregates import Sum, Count, Avg, Variance, StdDev, Max, Min
from datetime import datetime


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
        try:
            record = ConToday.objects.get(con_id=user.con_id)
            record.state = 1
            record.save()
        except ConToday.DoesNotExist:
            ConToday.objects.create(con_id=user.con_id, state=1, today_num=0, now_num=0)
    if Director.objects.filter(username=username).count() != 0:
        user = Director.objects.get(username=username)
        try:
            record = DirToday.objects.get(con_id=user.dir_id)
            record.state = 1
            record.save()
        except ConToday.DoesNotExist:
            DirToday.objects.create(con_id=user.con_id, state=1, today_num=0, now_num=0)

    if user == '':
        return 0
    if check_password(password, user.password):
        ticket = getToken()
        user.u_ticket = ticket
        user.save()

        return ticket
    else:
        return -1


def getToken():
    ticket = ''
    for i in range(15):
        s = 'abcdefghijklmnopqrstuvwxyz'
        ticket += random.choice(s)

    now_time = int(time.time())

    ticket = 'TK' + ticket + str(now_time)
    return ticket


def wCheckUser(form):
    name = form["name"]
    phon_number = form["phon_number"]
    sos_name = form["sos_name"]
    sos_phonnumber = form["sos_phonnumber"]
    ticket = getToken()
    try:
        user = Visitor.objects.get(name=name, tele=phon_number)
        user.u_ticket = ticket
        user.save()
        return ticket, "Successfully login!"
    except Visitor.DoesNotExist:
        Visitor.objects.create(name=name, tele=phon_number,
                               emer_name=sos_name, emer_tele=sos_phonnumber, date=datetime.now())
        return ticket, "This is a new User"


def getDashboardConsultant(token):
    try:
        Consultant.objects.get(u_ticket=token)
        user_info = Consultant.objects.get(u_ticket=token)
    except Consultant.DoesNotExist:
        return '', 'Consultant err'
    try:
        today_info = ConToday.objects.get(con_id=user_info.con_id)
    except ConToday.DoesNotExist:
        return '', 'ConToday err'

    try:
        conschedule = ConSchedule.objects.filter(con_id=user_info.con_id)
    except ConSchedule.DoesNotExist:
        return '', 'ConSchedule err'

    calendar = []
    for sch in conschedule:
        list = convert.get_date(sch.weekday)
        for i in list:
            calendar.append(i)

    tableData = []
    try:
        records = VisitorConRecord.objects.filter(con_id=user_info.con_id).order_by('-stime')[:5]
        for record in records:
            try:
                name = Visitor.objects.get(vis_id=record.vis_id).name
            except Visitor.DoesNotExist:
                continue
            ele = {
                'id': record.vis_con_id,
                'name': name,
                'time': convert.timeChange(record.duration),
                'date': record.stime.strftime("%Y-%m-%d %H:%M:%S"),
                'rate': record.v2c_score,
                'comment': record.v2c_comm,
            }
            tableData.append(ele)
    except VisitorConRecord.DoesNotExist:
        return '', 'VisitorConRecord Does Not Exist'

    data = {
        'tableData': tableData,
        'rate': user_info.av_score,
        'squareUrl': user_info.icon,
        'consultNum': user_info.totel_num,
        'consultTodayNum': today_info.today_num,
        'consultTodayTime': convert.timeChange(today_info.today_dur),
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
            username = Visitor.objects.get(vis_id=record.vis_id).name
            ele = {
                'id': record.vis_con_id,
                'name': username,
                'time': convert.timeChange(record.duration),
                'date': record.stime.strftime("%Y-%m-%d %H:%M:%S"),
                'rate': record.v2c_score,
                'comment': record.v2c_comm
            }
            list.append(ele)

    return list, ''


def getDashboardDirector(token):
    try:
        user_info = Director.objects.get(u_ticket=token)
    except Director.DoesNotExist:
        return '', 'Director No Data'

    try:
        consults = Consultant.objects.filter(dir_id=user_info.dir_id)
    except Consultant.DoesNotExist:
        return '', 'No consultant'

    try:
        dirSchedule = DirSchedule.objects.filter(dir_id=user_info.dir_id)
    except DirSchedule.DoesNotExist:
        return '', 'DirSchedule err'

    conlist = []
    for consult in consults:
        try:
            today = ConToday.objects.get(con_id=consult.con_id, state=1)
            data = {
                'name': consult.username,
                'state': today.state
            }
            conlist.append(data)
        except:
            data = {}

    tableData = []
    records = ConDirRecord.objects.filter(dir_id=user_info.dir_id).order_by('-stime')[0:5]
    for record in records:
        consult = Consultant.objects.get(con_id=record.con_id)
        data = {
            'id': record.con_dir_id,
            'name': consult.username,
            'time': convert.timeChange(record.duration),
            'date': record.stime.strftime("%Y-%m-%d %H:%M:%S"),
        }
        tableData.append(data)
    today_info = DirToday.objects.get(dir_id=user_info.dir_id)

    calendarData = []
    for sch in dirSchedule:
        list = convert.get_date(sch.weekday)
        for i in list:
            calendarData.append(i)

    res = {
        'consultList': conlist,
        'consultNum': today_info.today_num,
        'directorName': user_info.username,
        'today_num': today_info.today_num,
        'today_time': convert.timeChange(today_info.today_dur),
        'squarUrl': user_info.icon,
        'tableData': tableData,
        'calendarData': calendarData,
    }

    return res, ''


def getRecordDirector(username, begin_date, end_date):
    if username == '':
        consultants = Consultant.objects.all()
    else:
        try:
            consultants = Consultant.objects.filter(username=username)
        except Consultant.DoesNotExist:
            return [], 'No such consultant'
    list = []
    if consultants.count() == 0:
        return [], 'No such consultant'
    for consultant in consultants:
        try:
            records = ConDirRecord.objects.filter(con_id=consultant.con_id, stime__range=[begin_date, end_date])
        except ConDirRecord.DoesNotExist:
            continue
        for record in records:
            username = Consultant.objects.get(con_id=record.con_id).username
            ele = {
                'id': record.con_dir_id,
                'name': username,
                'time': convert.timeChange(record.duration),
                'date': record.stime.strftime(("%Y-%m-%d %H:%M:%S")),
            }
            list.append(ele)

    return list, ''


def getRecordAdmin(username, begin_date, end_date):
    if username == '':
        visitors = Visitor.objects.all()
    else:
        try:
            visitors = Visitor.objects.filter(name=username)
        except Visitor.DoesNotExist:
            return '', 'Visitor: No data'

    list = []
    for visitor in visitors:
        try:
            records = VisitorConRecord.objects.filter(vis_id=visitor.vis_id, stime__range=[begin_date, end_date])
        except VisitorConRecord.DoesNotExist:
            continue
        for record in records:
            ele = {
                'id': record.vis_con_id,
                'name': visitor.name,
                'time': convert.timeChange(record.duration),
                'date': record.stime.strftime(("%Y-%m-%d %H:%M:%S")),
                'rate': record.v2c_score,
                'eva': record.v2c_comm,
                'assit': 'No Record'
            }
            list.append(ele)

    data = {
        'list': list,
        'total': len(list)
    }
    return data, ''


def getConsultantManage(username):
    if username == '':
        consults = Consultant.objects.all()
    else:
        try:
            consults = Consultant.objects.filter(username=username)
        except Consultant.DoesNotExist:
            return '', 'Consultant: No Data'
    list = []
    if consults.count() == 0:
        return '', 'Consultant: Not Exist!'
    for consult in consults:
        monitor = Director.objects.get(dir_id=consult.dir_id).username
        sches = ConSchedule.objects.filter(con_id=consult.con_id)
        weekday = []
        for sche in sches:
            weekday.append(sche.weekday)
        if consult.totel_dur is None:
            dur = 0
        else:
            dur = consult.totel_dur

        data = {
            'id': consult.con_id,
            'name': consult.username,
            'monitor': monitor,
            'sum': consult.totel_num,
            'time': convert.timeChange(dur),
            'rate': consult.av_score,
            'schedule': ",".join(weekday)
        }
        list.append(data)
    monitorList = getDirectorList()

    return list, monitorList, ''


def getMonitorAdmin(name):
    if name == '':
        directors = Director.objects.all()
    else:
        directors = Director.objects.filter(username=name)
    list = []
    qualList = []
    if directors.count() == 0:
        return []
    for director in directors:
        consultants = Consultant.objects.filter(dir_id=director.dir_id)
        coList = []
        for consultant in consultants:
            username = consultant.username
            if username not in coList:
                coList.append(username)
        consol = ",".join(coList)
        sches = DirSchedule.objects.filter(dir_id=director.dir_id)
        weekdayList = []
        for sche in sches:
            weekdayList.append(sche.weekday)
        sum = director.number
        time = director.duration
        qual = {
            "qualName": director.qual,
            "qualId": director.qualnum
        }
        data = {
            'id': director.dir_id,
            'name': director.username,
            'consultant': consol,
            'sum': sum,
            'time': convert.timeChange(time),
            'schedule': ",".join(weekdayList)
        }
        qualList.append(qual)
        list.append(data)

    return list, qualList


def getUserAdmin(username):
    if username == '':
        users = Visitor.objects.filter(type=constants.Visitor)
    else:
        users = Visitor.objects.filter(name=username, type=constants.Visitor)
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
    except Visitor.DoesNotExist:
        return '', 'User is not admin'

    if admin.count() == 0:
        return '', 'User is not admin'

    consultantList = getOnCallConsultantList()
    directorList = getOnCallDirectorList()

    consultNum = ConToday.objects.filter(state=1).count()
    chatNum = DirToday.objects.filter(state=1).count()
    consultTodayNum = ConToday.objects.aggregate(nums=Sum('today_num'))['nums']
    consultTodayTime = ConToday.objects.all().aggregate(duration=Sum('today_dur'))['duration']

    firstDay = convert.get_past_week()
    weekchartDatas = VisitorConRecord.objects.filter(stime__gte=firstDay).order_by("-stime")

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

    def takeFirst(elem):
        return elem[0]

    weekChartData.sort(key=takeFirst)

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

    consultants = Consultant.objects.all().order_by('-totel_num')[:4]
    sumList = []

    for consult in consultants:
        data = {
            'photo': consult.icon,
            'name': consult.username,
            'consultNum': consult.totel_num
        }
        sumList.append(data)

    rateList = []
    consultants = Consultant.objects.all().order_by('-av_score')[:4]

    for consult in consultants:
        data = {
            'photo': consult.icon,
            'name': consult.username,
            'consultNum': consult.av_score
        }

        rateList.append(data)

    res = {
        'oncallConsult': consultantList,
        'oncallMonitor': directorList,
        'consultNum': consultNum,
        'chatNum': chatNum,
        'consultTodayNum': consultTodayNum,
        'consultTodayTime': convert.timeChange(consultTodayTime),
        'myChartData': myChartData,
        'weekChartData': weekChartData,
        'sumList': sumList,
        'rateList': rateList,
    }

    return res, ''


def getDirectorList():
    try:
        dirctors = Director.objects.all()
    except Director.DoesNotExist:
        return '', 'Director err'

    directorList = []
    for dirctor in dirctors:
        data = {
            'name': dirctor.username,
            'monitorId': dirctor.dir_id
        }

        directorList.append(data)

    return directorList


def getConsultantList():
    try:
        consultants = Consultant.objects.all()
    except Consultant.DoesNotExist:
        return '', 'Consultant err'

    consultantList = []
    for consultant in consultants:
        data = {
            'name': consultant.username,
            'consultantId': consultant.con_id
        }
        consultantList.append(data)

    return consultantList


def getOnCallConsultantList():
    try:
        consultants = Consultant.objects.all()
    except Consultant.DoesNotExist:
        return '', 'Consultant err'

    consultantList = []
    for consultant in consultants:
        try:
            state = ConToday.objects.get(con_id=consultant.con_id).state
            if state != 1:
                continue
            else:
                data = {
                    'name': consultant.username,
                    'consultantId': consultant.con_id
                }
                consultantList.append(data)
        except ConToday.DoesNotExist:
            continue

    return consultantList


def getOnCallDirectorList():
    try:
        directors = Director.objects.all()
    except Director.DoesNotExist:
        return '', 'Consultant err'

    directorList = []
    for director in directors:
        try:
            state = DirToday.objects.get(dir_id=director.dir_id).state
            if state != 1:
                continue
            else:
                data = {
                    'name': director.username,
                    'monitorId': director.dir_id
                }
                directorList.append(data)
        except DirToday.DoesNotExist:
            continue

    return directorList


def getScheduleEvent():
    records = ConSchedule.objects.all()
    dict = {
        'Mon': 0,
        'Tue': 0,
        'Wed': 0,
        'Thu': 0,
        'Fri': 0,
        'Sat': 0,
        'Sun': 0
    }
    for record in records:
        dict[record.weekday] = dict[record.weekday] + 1

    thisWeek = convert.getThisWeekDict()
    events = []
    for k, v in dict.items():
        ele = {
            'title': "咨询师： " + str(v),
            'start': thisWeek.get(k)
        }
        events.append(ele)
    ddict = {
        'Mon': 0,
        'Tue': 0,
        'Wed': 0,
        'Thu': 0,
        'Fri': 0,
        'Sat': 0,
        'Sun': 0
    }
    drecords = DirSchedule.objects.all()
    for r in drecords:
        ddict[r.weekday] = ddict[r.weekday] + 1
    for k, v in ddict.items():
        ele = {
            'title': "督导： " + str(v),
            'start': thisWeek.get(k)
        }
        events.append(ele)

    return events


def getScheduleQuery(date):
    weekday = convert.getWeekDay(date)
    try:
        recordsConsul = ConSchedule.objects.filter(weekday=weekday)
    except ConSchedule.DoesNotExist:
        return '', 'ConSchedule: ' + date + ' no scehdule'

    consultantList = []
    for record in recordsConsul:
        name = Consultant.objects.get(con_id=record.con_id).username
        if name not in consultantList:
            consultantList.append(name)

    consultantName = ",".join(consultantList)

    try:
        recordsMonitor = DirSchedule.objects.filter(weekday=weekday)
    except DirSchedule.DoesNotExist:
        return '', 'DirSchedule: ' + date + ' no scehdule'

    monitorList = []
    for record in recordsMonitor:
        name = Director.objects.get(dir_id=record.dir_id).username
        if name not in monitorList:
            monitorList.append(name)

    monitorName = ",".join(monitorList)

    res = {
        'consultantName': consultantName,
        'monitorName': monitorName
    }
    return res, ''


def addConsultantShcedule(addForm):
    consultantId = addForm['consultantId']
    monitorId = addForm['monitorId']
    dateValue = addForm['dateValue']
    err = ''
    date = datetime.strptime(dateValue, "%Y-%m-%d")
    if monitorId != '':
        try:
            monitor = Director.objects.get(dir_id=monitorId)
            # date = datetime.strptime("2022-04-17", "%Y-%m-%d")
            weekday = convert.getWeekDay(date)
            try:
                DirSchedule.objects.get(dir_id=monitor.dir_id, weekday=weekday)
            except DirSchedule.DoesNotExist:
                DirSchedule.objects.create(dir_id=monitor.dir_id, weekday=weekday)
        except Director.DoesNotExist:
            err += "No Such monitor please register first"

    if consultantId != '':
        try:
            consultant = Consultant.objects.get(con_id=consultantId)
            weekday = convert.getWeekDay(date)
            try:
                ConSchedule.objects.get(con_id=consultant.con_id, weekday=weekday)
            except ConSchedule.DoesNotExist:
                ConSchedule.objects.create(con_id=consultant.con_id, weekday=weekday)
        except Consultant.DoesNotExist:
            err += "No Such consultant please register first"

    return err


def addConsultantItem(form):
    err = checkForm(form)
    if err != '':
        return err
    name = form["name"]
    gender = form["gender"]
    age = form["age"]
    identity = form["idNumber"]
    phone = form["phone"]
    email = form["email"]
    dir_id = form["monitorId"]
    username = form["userName"]
    password = make_password(form["pwd"])
    company = form["company"]
    title = form["rank"]

    Consultant.objects.create(name=name, sex=gender, age=age,
                              identity=identity, tele=phone, email=email,
                              dir_id=dir_id, username=username, password=password,
                              unit=company, title=title, totel_num=0, totel_dur=0, av_score=0)
    return ''


def checkForm(form):
    for k, v in form.items():
        if v == '':
            return k + " isn't given."
    return ''


def editConsultantItem(form):
    editName = form['name']
    dir_id = form['monitor']
    schedules = form['schedule']
    scheduleList = schedules.split("&")
    con_id = form['id']
    err1 = ''
    err2 = ''
    try:
        consultant = Consultant.objects.get(con_id=con_id)
        if editName != '':
            consultant.username = editName

        if dir_id != '':
            consultant.dir_id = dir_id

        consultant.save()
        try:
            ConSchedule.objects.filter(con_id=consultant.con_id).delete()
        except ConSchedule.DoesNotExist:
            err1 = "This is the first time to set its schedule."
        for sche in scheduleList:
            day = sche.split("=")
            ConSchedule.objects.create(con_id=consultant.con_id, weekday=day[1])
    except Consultant.DoesNotExist:
        err2 = "No such consultant please register first"

    return err1, err2


def addDirectorItem(form):
    err = checkForm(form)
    if err != '':
        return err
    name = form["name"]
    gender = form["gender"]
    age = form["age"]
    identity = form["idNumber"]
    phone = form["phone"]
    email = form["email"]
    username = form["userName"]
    password = make_password(form["pwd"])
    company = form["company"]
    title = form["rank"]
    qual = form["qualId"]
    qualNum = form["certId"]

    Director.objects.create(name=name, sex=gender, age=age, identity=identity,
                            tele=phone, email=email, username=username,
                            password=password, unit=company, title=title, qual=qual, qualnum=qualNum,
                            number=0, duration=0)
    return ''


def editDirectorItem(form):
    editName = form['name']
    schedules = form['schedule']
    scheduleList = schedules.split("&")
    dir_id = form['id']
    msg = ''

    try:
        director = Director.objects.get(dir_id=dir_id)
        if editName != '':
            director.username = editName

        director.save()

        try:
            DirSchedule.objects.filter(dir_id=director.dir_id).delete()
        except DirSchedule.DoesNotExist:
            msg = 'This is the first time to set the schedule of director.'

        for schedule in scheduleList:
            day = schedule.split("=")
            DirSchedule.objects.create(dir_id=director.dir_id, weekday=day[1])

        return msg, ''
    except Director.DoesNotExist:
        return '', 'No such director, please register it first.'


def banVisitor(name):
    try:
        visitors = Visitor.objects.filter(name=name)

        for visitor in visitors:
            visitor.ban = 0
            visitor.save()

        return ''
    except Visitor.DoesNotExist:
        return 'No such visitor, please register first.'


def getDetails(id, type):
    if id == '':
        return '', "id is None."
    if type == "0":
        try:
            meetingID = ConDirRecord.objects.get(con_dir_id=id).record
        except ConDirRecord.DoesNotExist:
            return '', "Doesn't have such record."
    else:
        try:
            meetingID = VisitorConRecord.objects.get(vis_con_id=id).record
        except VisitorConRecord.DoesNotExist:
            return '', "Doesn't have such record."

    records = Record.objects.filter(im_id=meetingID)
    content = []
    for record in records:
        data = {
            "name": record.user_name,
            "timestamp": datetime.timestamp(record.create_time),
            "payload": {"text": record.msg_text}
        }
        content.append(data)

    return content, ''


def changeState(token):
    try:
        consult = Consultant.objects.get(u_ticket=token)
        try:
            record = ConToday.objects.get(con_id=consult.con_id)
            record.state = 0
            record.save()
            return "Success!"
        except ConToday.DoesNotExist:
            return "Success!"
    except Consultant.DoesNotExist:
        try:
            director = Director.objects.get(u_ticket=token)
            try:
                record = DirToday.objects.get(dir_id=director.dir_id)
                record.state = 0
                record.save()
                return "Success!"
            except DirToday.DoesNotExist:
                return "Success!"
        except Director.DoesNotExist:
            return "Success!"


def getAllOnlineConsultant(token):
    visitor = Visitor.objects.get(u_ticket=token)
    records = ConToday.objects.filter(state=1)
    consultList = []
    for record in records:
        try:
            consultant = Consultant.objects.get(con_id=record.con_id)
            avator = consultant.icon
            name = consultant.username
            rate = consultant.av_score
            try:
                status = ConToday.objects.get(con_id=consultant.con_id).state
            except ConToday.DoesNotExist:
                status = 0

            if VisitorConRecord.objects.filter(con_id=consultant.con_id, vis_id=visitor.vis_id).count() > 0:
                isConsulted = 1
            else:
                isConsulted = 0

            data = {
                "avator": avator,
                "name": name,
                "rate": rate,
                "status": status,
                "isConsulted": isConsulted
            }
            consultList.append(data)
        except Consultant.DoesNotExist:
            continue

    return consultList


def addTalkingRecord(form):
    uu_id = form["uu_id"]
    evaluate = form["evaluate"]
    record = "Wait"
    con_id = form["con_id"]
    stime = datetime.now()

    try:
        record = VisitorConRecord.objects.get(vis_id=uu_id, con_id=con_id, v2c_score=-1)
        record.v2c_score = evaluate
        record.stime = stime
        record.save()
    except VisitorConRecord.DoesNotExist:
        if VisitorConRecord.objects.filter(vis_id=uu_id, con_id=con_id).count() > 0:
            his_state = 1
        else:
            his_state = 0

        VisitorConRecord.objects.create(vis_id=uu_id, v2c_score=evaluate, record=record,
                                        stime=stime, con_id=con_id, his_state=his_state)


def getHistoryConversation(token):
    try:
        visitor = Visitor.objects.get(u_ticket=token)
        conversionList = []
        try:
            records = VisitorConRecord.objects.filter(vis_id=visitor.vis_id)
            for record in records:
                consult = Consultant.objects.get(con_id=record.con_id)
                consultants = {
                    "avator": consult.icon,
                    "name": consult.username
                }
                startTime = record.stime
                try:
                    state = ConToday.objects.get(con_id=consult.con_id).state
                except ConToday.DoesNotExist:
                    state = 0

                duration = record.duration
                evaluate = record.v2c_score
                data = {
                    'consultants': consultants,
                    "startTime": startTime.strftime("%Y-%m-%d %H:%M:%S"),
                    "state": state,
                    "duration": duration,
                    "evaluate": evaluate
                }
                print(data)
                conversionList.append(data)
            return conversionList, ''
        except VisitorConRecord.DoesNotExist:
            return conversionList, ''
    except Visitor.DoesNotExist:
        return '', 'No such Visitor'


def getUserList():
    visitors = Visitor.objects.all()

    content = []
    for visitor in visitors:
        data = {
            "avatar": visitor.icon,
            "name": visitor.name,
            "uuid": "user-" + str(visitor.vis_id)
        }

        content.append(data)

    return content


def askForDir(token):
    consultant = Consultant.objects.get(u_ticket=token)
    director = Director.objects.get(dir_id=consultant.dir_id)
    content = []
    data = {
        "avator": director.icon,
        "name": director.username,
        "uuid": "director-" + str(director.dir_id)
    }

    content.append(data)
    return content


def getIMRecord(id, type):
    if type == "0":
        record_id = ConDirRecord.objects.get(con_dir_id=id).record
    else:
        record_id = VisitorConRecord.objects.get(vis_con_id=id).record

    records = Record.objects.filter(im_id=record_id)
    content = []
    for record in records:
        data = {
            "record_id": record.im_id,
            "sendername": record.user_name,
            "timestamp": datetime.timestamp(record.create_time),
            "type": record.type,
            "content": record.msg_text
        }
        content.append(data)

    return content


def saveCVRecord(form):
    vis_name = form["vis_name"]
    con_name = form["con_name"]
    duration = form["time"]
    date = datetime.strptime(form["date"], "%Y-%m-%d %H:%M:%S")
    id = form["id"]
    try:
        consultant = Consultant.objects.get(username=con_name)
    except Consultant.DoesNotExist:
        return "No Such Consultant."

    try:
        visitor = Visitor.objects.get(name=vis_name)
    except Visitor.DoesNotExist:
        return "No Such Visitor."

    try:
        record = VisitorConRecord.objects.get(con_id=consultant.con_id, vis_id=visitor.vis_id, record="Wait")
        record.record = id
        record.duration = duration
        record.stime = date
        record.save()
        return ""
    except VisitorConRecord.DoesNotExist:
        if VisitorConRecord.objects.filter(vis_id=visitor.vis_id, con_id=consultant.con_id).count() > 0:
            his_state = 1
        else:
            his_state = 0
        VisitorConRecord.objects.create(con_id=consultant.con_id, record=id, duration=duration,
                                        stime=date, vis_id=visitor.vis_id, v2c_score=-1, his_state=his_state)
        return ""


def saveCDRecord(form):
    id = form["id"]
    con_name = form["con_name"]
    dir_name = form["dir_name"]
    time = form["time"]
    date = datetime.strptime(form["date"], "%Y-%m-%d %H:%M:%S")

    try:
        consultant = Consultant.objects.get(username=con_name)
    except Consultant.DoesNotExist:
        return "No Such Consultant."

    try:
        director = Director.objects.get(username=dir_name)
    except Director.DoesNotExist:
        return "No Such Director."

    ConDirRecord.objects.create(con_id=consultant.con_id, dir_id=director.dir_id,
                                record=id, stime=date, duration=time)

    return ""
