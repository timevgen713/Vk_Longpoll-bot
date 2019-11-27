import pytz
import datetime
from time import strftime, gmtime

utc = pytz.utc
msk = pytz.timezone('Europe/Moscow')

def time_now():
	# время по мск
	return datetime.datetime.now(tz=msk).strftime('%H:%M:%S')
def time_nowdate():
	# time_now() без перевода результата в строку
	return datetime.datetime.now(tz=msk)
def datetime_now():
	# время и дата по мск
	 return datetime.datetime.now(tz=msk).strftime('%Y-%m-%d %H:%M:%S')
def date_now():
	# дата по мск
	return datetime.datetime.now(tz=msk).strftime('%Y-%m-%d')
def time_add(delta):
	# сложение дат
	now = time_nowdate()
	add = delta.split('.')
	add = list(map(int, add))
	d = datetime.timedelta(hours=add[0], minutes=add[1],seconds=add[2])
	res = now + d
	res = str(res)
	return res[:19:]
