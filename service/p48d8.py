import os
import sys
import time
from time import sleep
import socket
import threading
import MySQLdb
import gc
import urllib.request
import json
import linecache

mysqlHost = "localhost"
mysqlUser = "editor"
mysqlPass = "9qtrnB5T9P74kNa7"

def ConnectToDataBase(user, passwd, db):
	conn = MySQLdb.connect(host=mysqlHost, user=user, passwd=passwd, db=db)
	cur = conn.cursor(MySQLdb.cursors.DictCursor)
	return conn, cur
#end define

def DataBaseRequest(conn, cur, sql):
	try:
		result = cur.execute(sql)
		row = cur.fetchall()
		buffer = sql.lower()
		if "select" not in buffer:
			conn.commit()
		return row, result
	except MySQLdb.Error as err:
		AddLog("DataBaseRequest: " + sql, "debug")
		AddLog("DataBaseRequest: " + str(err), "error")
		return
#end define

def DataBaseConnectionClose(conn, cur):
	cur.close()
	conn.close()
	gc.collect()
#end define

def AddLog(inputText, mode="info"):
	localDate = time.strftime('%d.%m.%Y, %H:%M:%S'.ljust(21, " "))
	modeText = (' [' + mode + '] ').ljust(10, " ")
	text = localDate + modeText + inputText
	logName = (sys.argv[0])[:(sys.argv[0]).rfind('.')]
	file = open(logName + ".log", 'a')
	file.write(text + "\r\n")
	file.close()
	print(text)
#end define

def General():
	AddLog("General")
	
	while True:
		r = P32()
		if r==1:
			return
#end define

def P32():
	global cid
	AddLog("P32:" + str(cid))
	cid-=1;
	conn = MySQLdb.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPass, db="schistory")
	sql = "select * from clanshistory where cid=" + str(cid)
	cur = conn.cursor(MySQLdb.cursors.DictCursor)
	result = cur.execute(sql)

	if result==0:
		return 1
	limit = result - 1
	sql = "delete from clanshistory where cid=" + str(cid) + " order by chid desc limit " + str(limit)
	result = cur.execute(sql)
	conn.commit()
	#print(sql)
	
	cur.close()
	conn.close()
	gc.collect()
	return 0
#end define



myName = (sys.argv[0])[:(sys.argv[0]).rfind('.')]
logName = myName + ".log"
cid=0

if os.path.isfile(logName):
	os.remove(logName)
#end if


try:
	General()
except BaseException as err:
	AddLog("Critical error: " + str(err) + str(sys.exc_info()), 'error')
#end try
