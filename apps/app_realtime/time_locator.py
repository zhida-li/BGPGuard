# Apr. 28, 2020
import time
import datetime


# time.gmtime()
# time.struct_time(tm_year=2020, tm_mon=4, tm_mday=27, tm_hour=8, tm_min=10,
# tm_sec=10, tm_wday=0, tm_yday=118, tm_isdst=0)

# Enter RIPE or RouteViews
def time_locator_single(site):
    gmtime_now = time.gmtime()
    year = gmtime_now.tm_year
    year = str(year)

    month = gmtime_now.tm_mon
    month = str(month)
    if len(month) == 2:
        pass
    else:
        month = '0' + month

    day = gmtime_now.tm_mday
    day = str(day)
    if len(day) == 2:
        pass
    else:
        day = '0' + day

    hour = gmtime_now.tm_hour
    hour = str(hour)
    if len(hour) == 2:
        pass
    else:
        hour = '0' + hour

    if site == 'RIPE':
        minute = gmtime_now.tm_min
        if minute % 5 != 0:
            minute = minute - minute % 5

        minute = str(minute)
        if len(minute) == 2:
            pass
        else:
            minute = '0' + minute

        if minute == '00':
            minute = '55'
            hour = int(hour) - 1
            hour = str(hour)
            if len(hour) == 2:
                pass
            else:
                hour = '0' + hour
        else:
            minute = int(minute)
            minute = minute - 5
            minute = str(minute)
            if len(minute) == 2:
                pass
            else:
                minute = '0' + minute
    elif site == 'RouteViews':
        minute = gmtime_now.tm_min
        if minute % 15 != 0:
            minute = minute - minute % 15

        minute = str(minute)
        if len(minute) == 2:
            pass
        else:
            minute = '0' + minute

        if minute == '00':
            minute = '45'
            hour = int(hour) - 1
            hour = str(hour)
            if len(hour) == 2:
                pass
            else:
                hour = '0' + hour
        else:
            minute = int(minute)
            minute = minute - 15
            minute = str(minute)
            if len(minute) == 2:
                pass
            else:
                minute = '0' + minute
    else:
        print('Site name is incorrect.')
        exit()
    return year, month, day, hour, minute


# Return the all the dates in a list.
# format YYYYMMDD
def time_locator_multi(start_date, end_date):
    # start_date='20030121'
    # end_date='20030125'

    # time.strptime(time_string[, format])
    datestart = datetime.datetime.strptime(start_date, '%Y%m%d')
    dateend = datetime.datetime.strptime(end_date, '%Y%m%d')

    date_list = list()
    while datestart <= dateend:
        date_list.append(datestart.strftime('%Y%m%d'))
        datestart += datetime.timedelta(days=1)

    return date_list
