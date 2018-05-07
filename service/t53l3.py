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
mysqlPass = "5ohnn0"

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
	bigUserArray = [[]]
	conn = MySQLdb.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPass, db="sc_history_db")
	sql = "SELECT * FROM nickname_uid;"
	cur = conn.cursor(MySQLdb.cursors.DictCursor)
	result = cur.execute(sql)
	row = cur.fetchone()
	while row is not None:
		nickname = row['nickname']
		uid = row['uid']
		bigUserArray = bigUserArray + [[nickname, uid]]
		row = cur.fetchone()
	cur.close()
	conn.close()
	gc.collect()
	
	conn1, cur1 = ConnectToDataBase(mysqlUser, mysqlPass, "sc_history_db")

	for user in bigUserArray:
		if (len(user)!=2):
			continue
		uid = user[1]
		nickname = user[0]
		AddLog("user: " + nickname, "debug")
		webform_json = GetInformationFromHistory(str(uid))
		if webform_json == None:
			AddLog("I'm crying because I can't get a candy ;(", "error")
		elif webform_json['result'] < 1: # invalid nickname
			AddLog(webform_json['text'], "error")
		elif webform_json['result'] > 0: # If everything is ok
			AddUserHistoryInDB(conn1, cur1, webform_json)
			
	DataBaseConnectionClose(conn1, cur1)
#end define

def GetInformationFromHistory(uid):
	scURL = "http://ts2.scorpclub.ru/api/v2/userinfo.php?uid="
	for i in range(5):
		try:
			webform = (urllib.request.urlopen(scURL + uid).read()).decode("utf-8")
			webform_json = json.loads(webform)
			return webform_json
		except BaseException as err:
			AddLog("GetInformationFromSC: Attempt: " + str(i) + " " + str(err), "warning")
			sleep(i)
	return None
#end define

def AddUserHistoryInDB(conn1, cur1, webform_json):
	bigdata = webform_json['bigdata']
	AddLog("AddUserHistoryInDB: " + bigdata[0]['nickname'], "debug")
	
	
	
	for data in bigdata:
		data_now = data['date']
		
		sql = "SELECT * FROM uid_" + data['uid'] + " where DATE(date) = '" + data_now + "'"
		row, result = DataBaseRequest(conn1, cur1, sql)
		
		if (result == 0):
			WriteInToMySQL(data_now, conn1, cur1, data['uid'], data['nickname'], data)
#end define

def WriteInToMySQL(data_now, conn1, cur1, uid, nickname, data):
	AddLog("Start WriteInToMySQL " + str(uid), "debug")
	
	if uid != data['uid']:
		AddLog("WriteInToMySQL: uid from DB doesn't coincide with uid from SC", "warning")
		return
	#end if
	
	effRating = karma = prestigeBonus = gamePlayed = gameWin = totalAssists = totalBattleTime = totalDeath = totalDmgDone = totalHealingDone = totalKill = totalVpDmgDone = 0
	clanName = clanTag = ''
	
	serchText = 'effRating'
	if (serchText in data and data[serchText] != ""):
		effRating = int(float(data[serchText]))
	serchText = 'karma'	
	if (serchText in data and data[serchText] != ""):
		karma = int(float(data[serchText]))
	serchText = 'prestigeBonus'
	if (serchText in data and data[serchText] != ""):
		prestigeBonus = float(data[serchText]) # double
	#end if
	
	
	serchText = 'gamePlayed'
	if (serchText in data and data[serchText] != ""):
		gamePlayed = int(float(data[serchText]))
	serchText = 'gameWin'
	if (serchText in data and data[serchText] != ""):
		gameWin = int(float(data[serchText]))
	serchText = 'totalAssists'
	if (serchText in data and data[serchText] != ""):
		totalAssists = int(float(data[serchText]))
	serchText = 'totalBattleTime'
	if (serchText in data and data[serchText] != ""):
		totalBattleTime = int(float(data[serchText]))
	serchText = 'totalDeath'
	if (serchText in data and data[serchText] != ""):
		totalDeath = int(float(data[serchText]))
	serchText = 'totalDmgDone'
	if (serchText in data and data[serchText] != ""):
		totalDmgDone = int(float(data[serchText]))
	serchText = 'totalHealingDone'
	if (serchText in data and data[serchText] != ""):
		totalHealingDone = int(float(data[serchText]))
	serchText = 'totalKill'
	if (serchText in data and data[serchText] != ""):
		totalKill = int(float(data[serchText]))
	serchText = 'totalVpDmgDone'
	if (serchText in data and data[serchText] != ""):
		totalVpDmgDone = int(float(data[serchText]))
	#end if
	
	serchText = 'clanName'
	if (serchText in data and data[serchText] != ""):
		clanName = data[serchText]
	serchText = 'clanTag'
	if (serchText in data and data[serchText] != ""):
		clanTag = data[serchText]
	#end if
	
	WriteInTheUserHistory(data_now, conn1, cur1, uid, nickname, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag)
	
#end define

def WriteInTheUserHistory(data_now, conn, cur, uid, nickname, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag):
	sql = "INSERT INTO uid_" + str(uid) + " (date, uid, nickname, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag) VALUES ('" + data_now + "', '" + str(uid) + "', '" + str(nickname) + "', '" + str(effRating) + "', '" + str(karma) + "', '" + str(prestigeBonus) + "', '" + str(gamePlayed) + "', '" + str(gameWin) + "', '" + str(totalAssists) + "', '" + str(totalBattleTime) + "', '" + str(totalDeath) + "', '" + str(totalDmgDone) + "', '" + str(totalHealingDone) + "', '" + str(totalKill) + "', '" + str(totalVpDmgDone) + "', '" + clanName + "', '" + clanTag + "');"
	
	AddLog("INSERT INTO uid_" + str(uid) + " date: "  + data_now, "debug")
	
	DataBaseRequest(conn, cur, sql)
#end define


myName = (sys.argv[0])[:(sys.argv[0]).rfind('.')]
logName = myName + ".log"

if os.path.isfile(logName):
	os.remove(logName)
#end if


try:
	General()
except BaseException as err:
	AddLog("Critical error: " + str(err) + sys.exc_info(), 'error')
#end try


