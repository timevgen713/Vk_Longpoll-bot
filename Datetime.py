# TEST
import pytz
import datetime
from time import strftime, gmtime

utc = pytz.utc
msk = pytz.timezone('Europe/Moscow')


def msg_last_time_format():
    return strftime('%y.%m.%d', gmtime())

def time_now():
    # время по мск
    return datetime.datetime.now(tz=msk).strftime('%H:%M:%S MSK (UTC +3)')


def datetime_now():
    # время и дата по мск
    return datetime.datetime.now(tz=msk).strftime('%Y-%m-%d %H:%M:%S  MSK (UTC +3)')


def date_now():
    # дата по мск
    return datetime.datetime.now(tz=msk).strftime('%Y-%m-%d')
