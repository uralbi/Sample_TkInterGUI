import datetime
import time
import pyjokes

def min_sec(secs):
    mins = int(secs//60)
    hours = int(mins//60)
    secs = int(secs%60)
    if hours > 0:
        time_str = f'{hours}h {int(mins%60)}m {secs}s'
    elif mins == 0:
        time_str = f'{secs}s'
    else:
        time_str = f'{mins}m {secs}s'
    return time_str

def todo():
    todo_list = ''
    weekdays = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    td = datetime.date.today()

    td_d = td.day
    td_m = td.month
    td_y = td.year
    td_wd = td.weekday()

    n_year = td_y if td_m < 12 else (td_y + 1)
    n_month = td_m + 1 if td_m < 12 else 1

    mon1 = datetime.date(td.year, td_m, 1)
    mon2 = datetime.date(n_year, n_month, 1)

    t_days = (mon2 - mon1).days
    last_wd = datetime.date(td.year, td_m, t_days).weekday()

    if last_wd == 2:
        mbl_w2 = datetime.date(td.year, td_m, t_days)
        mbl_w1 = datetime.date(td.year, td_m, t_days - 7)
    elif last_wd < 2:
        mbl_w2 = datetime.date(td.year, td_m, t_days - (7 - last_wd - 2))
        mbl_w1 = datetime.date(td.year, td_m, t_days - (14 - last_wd - 2))
    elif last_wd > 2:
        mbl_w2 = datetime.date(td.year, td_m, t_days - (last_wd - 2))
        mbl_w1 = datetime.date(td.year, td_m, t_days - (last_wd - 2) - 7)

    if td_wd == 0:
        todo_list = 'KAM'
    elif td_wd == 1:
        todo_list = 'LEAD, PIERPASS'
    elif td == mbl_w2 or td == mbl_w1:
        todo_list = 'MBL'
    todo_list += f'  {weekdays[td_wd]} : {td_d} {td_m} {td_y}'
    return todo_list

def delay_mail(month, date, hour, min, function, message):
    curr_month = datetime.date.today().month
    curr_date = datetime.date.today().day
    set_m = month
    set_d = date
    set_time = datetime.time(hour,min,10)
    df_h = set_time.hour - datetime.datetime.now().hour
    df_m = set_time.minute - datetime.datetime.now().minute
    df_d = set_d - curr_date
    wait_mins = df_d*24*60 + df_h*60 + df_m
    if wait_mins < 0:
        print('Error: past date was set.')
        return
    print('Wait time:', min_sec(wait_mins*60))
    print('Running...')
    time.sleep(wait_mins*60)
    print('Time is up: ', datetime.datetime.now().hour,':', datetime.datetime.now().minute)
    function(f'{message}')

def current_date():
    day_d = datetime.date.today().day
    mon_m = datetime.date.today().month
    year_y = datetime.date.today().year
    curr_date = datetime.date.today()
    if len(str(day_d))<2:
        day_d = f'0{str(day_d)}'
    if len(str(mon_m))<2:
        mon_m = f'0{str(mon_m)}'
    str_date = f'{mon_m}{day_d}{year_y}'

    return str_date, curr_date

