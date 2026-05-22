import time
import datetime

dt = datetime.datetime(2024, 6, 1, 0, 0, 0)
print(dt)

print(time.time() // (3600*24*365.25))
dt = datetime.datetime.fromtimestamp(time.time())
print(dt)  

str_time = '2017/08/02 18:14:26'
form = '%Y/%m/%d %H:%M:%S'
dt = datetime.datetime.strptime(str_time, form)
print(dt)

another_form = '%Y/%m/%d %H/%M/%S'
dt_new_format = dt.strftime(another_form)
print(dt_new_format)

d = datetime.date(2017, 8, 2)
print(d.year, d.month, d.day)
print(d.strftime('%Y-%m-%d'))

t = datetime.time(18, 54, 32)
print(t.hour, t.minute, t.second, t.microsecond)
print(t.strftime('%H:%M:%S'))

day = datetime.date(2017, 8, 2)
time = datetime.time(18, 54, 32)
dt = datetime.datetime.combine(day, time)
print(dt)

dt = datetime.datetime(2017, 8, 2, 17, 29, 12, 34)
td = datetime.timedelta(days=5, hours=7, minutes=36, microseconds=10)
datetime_future = dt + td   # 往后推
datetime_past = dt - td     # 往前推
print(datetime_future)
print(datetime_past)

def last_week(s):
    form = '%Y-%m-%d'
    day = datetime.datetime.strptime(s, form)
    dt = day - datetime.timedelta(days=7)
    return dt.strftime(form)

print(last_week(datetime.datetime.now().strftime('%Y-%m-%d')))

def days(start, end):
    form = '%Y-%m-%d'
    start = datetime.datetime.strptime(start, form)
    end = datetime.datetime.strptime(end, form)
    delta = (end - start).days + 1
    if delta < 0:
        return 0
    return delta

print(days('2024-06-01', '2024-06-30'))