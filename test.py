import pymysql
import date
import datetime
###############################    chat_id и user_id  - строки #####################################
host = 'localhost'
user = 'root'
psw = ''
bd_name = 'vkbot'
'''def new_chat(chat_id,admin_id,members):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "CREATE TABLE `"+chat_id+"`(`id` text NOT NULL,`adminlvl` int(11) NOT NULL DEFAULT '0',`warns` int(11) NOT NULL DEFAULT '0',`mute` text NOT NULL,`ban` text NOT NULL,`msgcount` int(11) NOT NULL DEFAULT '0')"
	    cur.execute(sql)
	    for i in range(len(members)):
	    	if members[i]==admin_id:
	    		cur.execute("INSERT INTO `"+chat_id+"`(`id`) VALUES ('"+members[i]+"');")
	    		cur.execute("UPDATE`"+chat_id+"` SET `adminlvl`='1' WHERE `id`='"+admin_id+"';")
	    	else:
	    		cur.execute("INSERT INTO `"+chat_id+"`(`id`) VALUES ('"+members[i]+"');")'''
def db_promote(chat_id, user_id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "UPDATE `"+chat_id+"` SET `adminlvl`='1' WHERE `id`='"+user_id+"';"
	    cur.execute(sql)
def db_drop(chat_id, user_id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "UPDATE `"+chat_id+"` SET `adminlvl`='0' WHERE `id`='"+user_id+"';"
	    cur.execute(sql)

def db_msgcountadd(chat_id,user_id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `"+chat_id+"` WHERE `id`='"+user_id+"';"
	    cur.execute(sql)
	    rows = cur.fetchone()
	    msgcount = int(rows[3])+1
	    sql = "UPDATE `"+chat_id+"` SET `msgcount`='"+str(msgcount)+"' WHERE `id`='"+user_id+"';"
	    cur.execute(sql)
def db_get_msg_amount(chat_id, user_id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `"+chat_id+"` WHERE `id`='"+user_id+"';"
	    cur.execute(sql)
	    rows = cur.fetchone()
	    msgcount = int(rows[3])
	    return msgcount
def db_warn(chat_id,user_id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `"+chat_id+"` WHERE `id`='"+user_id+"';"
	    cur.execute(sql)
	    rows = cur.fetchone()
	    warns = int(rows[2])+1
	    if warns==3:
	    	# функция кика с беседы
	    	pass
def db_unwarn(chat_id, user_id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `"+chat_id+"` WHERE `id`='"+user_id+"';"
	    cur.execute(sql)
	    rows = cur.fetchone()
	    warns = int(rows[2])
	    if warns!=0:
	    	warns -=1
	    sql = "UPDATE `"+chat_id+"` SET `warns`='"+str(warns)+"' WHERE `id`='"+user_id+"';"
	    cur.execute(sql)
def db_getWarns(chat_id, user_id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "SELECT * FROM `"+chat_id+"` WHERE `id`='"+user_id+"';"
	    cur.execute(sql)
	    rows = cur.fetchone()
	    warns = int(rows[2])
	    return warns
def isAdmin(chat_id,user_id):
	con = pymysql.connect(host,user,psw,bd_name)
	with con:
		cur = con.cursor()
		sql = "SELECT * FROM `"+chat_id+"` WHERE `id`='"+user_id+"';"
		cur.execute(sql)
		rows = cur.fetchone()
		if rows==None:
			return False
		else:
			if rows[1]==1:
				return True
			else:
				return False
def db_msg_last_time_add(chat_id, user_id):
	con = pymysql.connect(host, user,psw, bd_name)
	with con:	    
	    cur = con.cursor()
	    sql = "UPDATE `"+chat_id+"` SET `last_message`='"+date.datetime_now()+"' WHERE `id`='"+user_id+"';"
	    cur.execute(sql)
def db_get_msg_last_time(chat_id, user_id):
	con = pymysql.connect(host,user,psw,bd_name)
	with con:
		cur = con.cursor()
		sql = "SELECT * FROM `"+chat_id+"` WHERE `id`='"+user_id+"';"
		cur.execute(sql)
		rows = cur.fetchone()
		return rows[4]
	
