import datetime


def timeChange(timeStep):
    hour = int(timeStep / (60 * 60))
    timeStep = timeStep - hour * 60 * 60
    min = int(timeStep / 60)
    timeStep -= min * 60
    second = timeStep

    return str(hour) + ':' + str(min) + ':' + str(second)


def get_past_week():
    today = datetime.date.today()
    days = datetime.timedelta(days=7)
    return today - days


def get_last_week():
    today = datetime.date.today()
    day_list = []
    for i in range(1, 7):
        today = today - datetime.timedelta(days=1)
        day_list.append(today)

    return day_list


def get_last_day():
    return datetime.datetime.now() - datetime.timedelta(hours=24)


def get_last_hour():
    today = datetime.datetime.now()
    hour_list = []
    for i in range(1, 24):
        today = today - datetime.timedelta(hours=1)
        hour_list.append(today)

    return hour_list


day_dict = {
    'Mon': 1,
    'Tue': 2,
    'Wed': 3,
    'Thu': 4,
    'Fri': 5,
    'Sat': 6,
    'Sun': 7
}


def get_date(day):
    m = datetime.datetime.now().month
    y = datetime.datetime.now().year
    ndays = (datetime.date(y, m + 1, 1) - datetime.date(y, m, 1)).days
    day_one = datetime.date(y, m, 1)
    last_day = datetime.date(y, m, ndays)
    delta = last_day - day_one
    data_list = []
    for i in range(delta.days + 1):
        p = (day_one + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        pp = datetime.datetime.strptime(str(p), '%Y-%m-%d')
        one = pp.isoweekday()
        if one == day_dict[day]:
            month = pp.strftime('%m')
            d = pp.strftime('%d')
            data = {
                'month': month,
                'day': d
            }
            data_list.append(data)
    return data_list


def getWeekDay(date):
    weekday = date.isoweekday()
    week_dict = {v: k for k, v in day_dict.items()}
    return week_dict.get(weekday)


def getThisWeekDict():
    today = datetime.datetime.now()
    dict = {}
    monday = today - datetime.timedelta(today.weekday())
    week_dict = {v: k for k, v in day_dict.items()}
    for i in range(0, 7):
        day = monday + datetime.timedelta(days=i)
        dict[week_dict.get(i + 1)] = day.strftime("%Y-%m-%d")

    return dict
