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