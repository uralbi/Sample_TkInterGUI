import time

def fns_log_file(info):
    curr_date = time.strftime('%D %H:%M')
    f = open('fnslog.txt', 'a')
    f.write(f'\n{curr_date} | {info}')
    f.close()