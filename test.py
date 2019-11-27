import pymysql
import Datetime
import datetime
host = 'localhost'
user = 'root'
psw = ''
bd_name = 'vkbot'
def bd_ban(id,time):
	res = date.time_add(time)
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "UPDATE `chatip` SET `ban`='"+res+"' WHERE `id`='"+id+"'"
	    cur.execute(sql)
def bd_unban(id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "UPDATE `chatip` SET `ban`='' WHERE `id`='"+id+"'"
	    cur.execute(sql)
def bd_bancheck():
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `chatip` WHERE `ban` is NOT NULL"
	    cur.execute(sql)
	    rows = cur.fetchall()
	    now = datetime.datetime.strptime(date.datetime_now(),'%Y-%m-%d %H:%M:%S')
	    for row in rows:
	    	try:
	    		unbandate = datetime.datetime.strptime(row[4],'%Y-%m-%d %H:%M:%S')
	    		if now>unbandate:
	    			bd_unban(row[0])
	    	except ValueError:
	    		pass
def bd_mute(id,time):
	res = date.time_add(time)
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "UPDATE `chatip` SET `mute`='"+res+"' WHERE `id`='"+id+"'"
	    cur.execute(sql)
def bd_unmute(id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "UPDATE `chatip` SET `mute`='' WHERE `id`='"+id+"'"
	    cur.execute(sql)
def bd_mutecheck():
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `chatip` WHERE `mute` is NOT NULL"
	    cur.execute(sql)
	    rows = cur.fetchall()
	    now = datetime.datetime.strptime(date.datetime_now(),'%Y-%m-%d %H:%M:%S')
	    for row in rows:
	    	try:
	    		unmutedate = datetime.datetime.strptime(row[3],'%Y-%m-%d %H:%M:%S')
	    		if now>unmutedate:
	    			bd_unmute(row[0])
	    	except ValueError:
	    		pass
def bd_promote(id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "UPDATE `chatip` SET `adminlvl`='1' WHERE `id`='"+id+"'"
	    cur.execute(sql)
def bd_drop(id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "UPDATE `chatip` SET `adminlvl`='0' WHERE `id`='"+id+"'"
	    cur.execute(sql)

def bd_msgcountadd(id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `chatip` WHERE `id`='"+id+"'"
	    cur.execute(sql)
	    rows = cur.fetchone()
	    msgcount = int(rows[5])+1
	    sql = "UPDATE `chatip` SET `msgcount`='"+str(msgcount)+"' WHERE `id`='"+id+"'"
	    cur.execute(sql)

def bd_warn(id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `chatip` WHERE `id`='"+id+"'"
	    cur.execute(sql)
	    rows = cur.fetchone()
	    warns = int(rows[2])+1
	    if warns>2:
	    	warns = 0
	    	bd_ban(id,'168.0.0')
	    sql = "UPDATE `chatip` SET `warns`='"+str(warns)+"' WHERE `id`='"+id+"'"
	    cur.execute(sql)
def bd_unwarn(id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `chatip` WHERE `id`='"+id+"'"
	    cur.execute(sql)
	    rows = cur.fetchone()
	    warns = int(rows[2])
	    if warns!=0:
	    	warns -=1
	    sql = "UPDATE `chatip` SET `warns`='"+str(warns)+"' WHERE `id`='"+id+"'"
	    cur.execute(sql)
