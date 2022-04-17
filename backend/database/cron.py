import datetime
from .models import *
from utils.convert import getWeekDay


def fresh_scheToday():
    try:
        weekday = getWeekDay(datetime.datetime.now())

        ConToday.objects.all().delete()

        conSches = ConSchedule.objects.filter(weekday=weekday)

        conTodayList = []
        for con in conSches:
            conTodayList.append(ConToday(con_id=con.con_id, state=0, today_num=0, today_dur=0, now_num=0))

        ConToday.objects.bulk_create(conTodayList)

        DirToday.objects.all().delete()
        dirSches = DirSchedule.objects.filter(weekday=weekday)

        dirTodayList = []
        for dir in dirSches:
            dirTodayList.append(DirToday(dir_id=dir.dir_id, today_num=0, today_dur=0, state=0))

        DirToday.objects.bulk_create(dirTodayList)
    except Exception as e:
        print('发生错误，错误信息为：', e)
