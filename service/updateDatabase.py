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


host = ''
port = 4800
packetLength = 2048

mysqlHost = "localhost"
mysqlUser = "editor"
mysqlPass = "5ohnn0"



def ConnectToDataBase(user, passwd, db):
	try:
		conn = MySQLdb.connect(host=mysqlHost, user=user, passwd=passwd, db=db)
		cur = conn.cursor(MySQLdb.cursors.DictCursor)
		return conn, cur
	except MySQLdb.Error as err:
		AddLog("ConnectToDataBase: " + str(err), "error")
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
#end define

def DataBaseConnectionClose(conn, cur):
	cur.close()
	conn.close()
	gc.collect()
#end define

def RememberLostUid(uid):
	isUidLost = True
	conn, cur = ConnectToDataBase(mysqlUser, mysqlPass, "sc_history_db")
	sql = "SELECT * FROM nickname_uid WHERE uid='" + str(uid) + "'"
	row, result = DataBaseRequest(conn, cur, sql)
	for user in row:
		webform_json = GetInformationFromSC(user['nickname'])
		if (webform_json != None and webform_json['code'] == 0 and user['uid'] == webform_json['data']['uid']):
			isUidLost = False
	if (isUidLost):
		sql = "INSERT INTO lost_uids (uid) VALUES ('" + str(uid) + "')"
		DataBaseRequest(conn, cur, sql)
	DataBaseConnectionClose(conn, cur)
#end define

def ScanInformation(row):
	AddLog("Start ScanInformation", "debug")
	
	try:
		conn1, cur1 = ConnectToDataBase(mysqlUser, mysqlPass, "sc_history_db")
		conn2, cur2 = ConnectToDataBase(mysqlUser, mysqlPass, "sc_clan_db")
		data_now = time.strftime('%Y-%m-%d')
		for user in row:
			uid = user['uid']
			nickname = user['nickname']
			webform_json = GetInformationFromSC(nickname)
			if webform_json == None:
				AddLog("I'm crying because I can't get a candy ;(", "error")
			elif webform_json['code'] == 1: # If invalid nickname
				RememberLostUid(uid)
				DeleteInTheTop100(uid)
			elif webform_json['code'] == 0: # If everything is ok
				data = webform_json['data']
				WriteInToMySQL(data_now, conn1, conn2, cur1, cur2, uid, nickname, data)
		DataBaseConnectionClose(conn1, cur1)
		DataBaseConnectionClose(conn2, cur2)
	except Exception as err:
		AddLog("Critical error: " + str(err), "error")
#end define

def General():
	AddLog("Start General function", "debug")
	RecordStartTime()
	
	# Clear Lost Uids
	conn, cur = ConnectToDataBase(mysqlUser, mysqlPass, "sc_history_db")
	row, result = DataBaseRequest(conn, cur, "DELETE FROM lost_uids")
	DataBaseConnectionClose(conn, cur)
	
	# Find all users in DB
	conn, cur = ConnectToDataBase(mysqlUser, mysqlPass, "sc_history_db")
	row, result = DataBaseRequest(conn, cur, "SELECT * FROM nickname_uid")
	DataBaseConnectionClose(conn, cur)
	
	# Discover all user from SC
	threadNumber = 10
	chunkRow = chunkIt(row, threadNumber)
	for i in range(threadNumber):
		threading.Thread(target=ScanInformation, args=(chunkRow[i],)).start()
	while True:
		sleep(1)
		if (len(threading.enumerate()) == 1):
			break
	#end while
	
	RecordEndTime()
#end define

def WriteInToMySQL(data_now, conn1, conn2, cur1, cur2, uid, nickname, data):
	AddLog("Start WriteInToMySQL " + str(uid), "debug")
	
	if uid != data['uid']:
		AddLog("WriteInToMySQL: uid from DB doesn't coincide with uid from SC", "warning")
		return
	#end if
	
	effRating = karma = prestigeBonus = gamePlayed = gameWin = totalAssists = totalBattleTime = totalDeath = totalDmgDone = totalHealingDone = totalKill = totalVpDmgDone = 0
	clanName = clanTag = ''
	
	serchText = 'effRating'
	if (serchText in data):
		effRating = int(data[serchText])
	serchText = 'karma'	
	if (serchText in data):
		karma = int(data[serchText])
	serchText = 'prestigeBonus'
	if (serchText in data):
		prestigeBonus = float(data[serchText]) # double
	#end if
	
	serchText = 'pvp'
	if (serchText in data):
		pvp = data[serchText]
		serchText = 'gamePlayed'
		if (serchText in pvp):
			gamePlayed = int(pvp[serchText])
		serchText = 'gameWin'
		if (serchText in pvp):
			gameWin = int(pvp[serchText])
		serchText = 'totalAssists'
		if (serchText in pvp):
			totalAssists = int(pvp[serchText])
		serchText = 'totalBattleTime'
		if (serchText in pvp):
			totalBattleTime = int(pvp[serchText])
		serchText = 'totalDeath'
		if (serchText in pvp):
			totalDeath = int(pvp[serchText])
		serchText = 'totalDmgDone'
		if (serchText in pvp):
			totalDmgDone = int(pvp[serchText])
		serchText = 'totalHealingDone'
		if (serchText in pvp):
			totalHealingDone = int(pvp[serchText])
		serchText = 'totalKill'
		if (serchText in pvp):
			totalKill = int(pvp[serchText])
		serchText = 'totalVpDmgDone'
		if (serchText in pvp):
			totalVpDmgDone = int(pvp[serchText])
	#end if
	
	serchText = 'clan'
	if (serchText in data):
		clan = data[serchText]
		serchText = 'name'
		if (serchText in clan):
			clanName = clan[serchText]
		serchText = 'tag'
		if (serchText in clan):
			clanTag = clan[serchText]
	#end if
	
	
	WriteInTheUserHistory(data_now, conn1, cur1, uid, nickname, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag)
	
	WriteInTheTop100(conn1, cur1, uid, nickname, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag)
	
	WriteInTheCorporationsHistory(data_now, conn2, cur2, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag)
	
#end define

def WriteInTheUserHistory(data_now, conn, cur, uid, nickname, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag):
	sql = "INSERT INTO uid_" + str(uid) + " (date, uid, nickname, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag) VALUES ('" + data_now + "', '" + str(uid) + "', '" + str(nickname) + "', '" + str(effRating) + "', '" + str(karma) + "', '" + str(prestigeBonus) + "', '" + str(gamePlayed) + "', '" + str(gameWin) + "', '" + str(totalAssists) + "', '" + str(totalBattleTime) + "', '" + str(totalDeath) + "', '" + str(totalDmgDone) + "', '" + str(totalHealingDone) + "', '" + str(totalKill) + "', '" + str(totalVpDmgDone) + "', '" + clanName + "', '" + clanTag + "');"
	
	DataBaseRequest(conn, cur, sql)
#end define

def WriteInTheCorporationsHistory(data_now, conn, cur, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag):
	AddLog("Start WriteInTheCorporationsHistory", "debug")
	
	# Return if user is not in the clan
	if (len(clanName) == 0):
		return
	
	sql = "SELECT * FROM corporations_history WHERE date='" + data_now + "' and BINARY clanName='" + clanName + "' and BINARY clanTag='" + clanTag + "'"
	row, result = DataBaseRequest(conn, cur, sql)
	
	if (result == 0):
		sql = "INSERT INTO corporations_history (date, clanName, clanTag, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, number) VALUES ('" + data_now + "', '" + clanName + "', '" + clanTag + "', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);"
		DataBaseRequest(conn, cur, sql)
	
	sql = "UPDATE corporations_history SET number = number + 1, effRating = effRating + " + str(effRating) + ", karma = karma + " + str(karma) + ", prestigeBonus = prestigeBonus + " + str(prestigeBonus) + ", gamePlayed = gamePlayed + " + str(gamePlayed) + ", gameWin = gameWin + " + str(gameWin) + ", totalAssists = totalAssists + " + str(totalAssists) + ", totalBattleTime = totalBattleTime + " + str(totalBattleTime) + ", totalDeath = totalDeath + " + str(totalDeath) + ", totalDmgDone = totalDmgDone + " + str(totalDmgDone) + ", totalHealingDone = totalHealingDone + " + str(totalHealingDone) + ", totalKill = totalKill + " + str(totalKill) + ", totalVpDmgDone = totalVpDmgDone + " + str(totalVpDmgDone) + " WHERE date = '" + data_now + "' and BINARY clanName = '" + clanName + "' and BINARY clanTag = '" + clanTag+ "'"
	
	DataBaseRequest(conn, cur, sql)
#end define

def WriteInTheTop100(conn, cur, uid, nickname, effRating, karma, prestigeBonus, gamePlayed, gameWin, totalAssists, totalBattleTime, totalDeath, totalDmgDone, totalHealingDone, totalKill, totalVpDmgDone, clanName, clanTag):
	sql = "SELECT * FROM top100 WHERE BINARY uid='" + str(uid) + "'"
	row, result = DataBaseRequest(conn, cur, sql)
	if result > 0:
		sql = "DELETE FROM top100 WHERE uid='" + str(uid) + "'"
		DataBaseRequest(conn, cur, sql)
	#end if
	
	effRating_old = karma_old = prestigeBonus_old = gamePlayed_old = gameWin_old = totalAssists_old = totalBattleTime_old = totalDeath_old = totalDmgDone_old = totalHealingDone_old = totalKill_old = totalVpDmgDone_old = 0
	
	if len(row) > 0:
		effRating_old = int(float(row[0]['effRating']))
		karma_old = int(float(row[0]['karma']))
		prestigeBonus_old = float(row[0]['prestigeBonus']) # double
		gamePlayed_old = int(float(row[0]['gamePlayed']))
		gameWin_old = int(float(row[0]['gameWin']))
		totalAssists_old = int(float(row[0]['totalAssists']))
		totalBattleTime_old = int(float(row[0]['totalBattleTime']))
		totalDeath_old = int(float(row[0]['totalDeath']))
		totalDmgDone_old = int(float(row[0]['totalDmgDone']))
		totalHealingDone_old = int(float(row[0]['totalHealingDone']))
		totalKill_old = int(float(row[0]['totalKill']))
		totalVpDmgDone_old = int(float(row[0]['totalVpDmgDone']))
	#end if
	
	if totalDeath != 0:
		kd = totalKill / totalDeath
		kda = (totalKill + totalAssists) / totalDeath
		kd = float("%.2f" % kd) # double
		kda = float("%.2f" % kda) # double
	else:
		kd = kda = 0
	if gamePlayed != 0:
		wr = gameWin / gamePlayed
		wr = float("%.2f" % wr) # double
	else:
		wr = 0
	if (gamePlayed - gameWin) != 0:
		wl = gameWin / (gamePlayed - gameWin)
		wl = float("%.2f" % wl) # double
	else:
		wl = gameWin / 1
	#end if
	
	effRating2 = effRating - effRating_old
	karma2 = karma - karma_old
	prestigeBonus2 = prestigeBonus - prestigeBonus_old
	gamePlayed2 = gamePlayed - gamePlayed_old
	gameWin2 = gameWin - gameWin_old
	totalAssists2 = totalAssists - totalAssists_old
	totalBattleTime2 = totalBattleTime - totalBattleTime_old
	totalDeath2 = totalDeath - totalDeath_old
	totalDmgDone2 = totalDmgDone - totalDmgDone_old
	totalHealingDone2 = totalHealingDone - totalHealingDone_old
	totalKill2 = totalKill - totalKill_old
	totalVpDmgDone2 = totalVpDmgDone - totalVpDmgDone_old
	
	if totalDeath2 != 0:
		kd2 = totalKill2 / totalDeath2
		kda2 = (totalKill2 + totalAssists2) / totalDeath2
		kd2 = float("%.2f" % kd2) # double
		kda2 = float("%.2f" % kda2) # double
	else:
		kd2 = kda2 = 0
	if gamePlayed2 != 0:
		wr2 = gameWin2 / gamePlayed2
		wr2 = float("%.2f" % wr2) # double
	else:
		wr2 = 0
	if (gamePlayed2 - gameWin2) != 0:
		wl2 = gameWin2 / (gamePlayed2 - gameWin2)
		wl2 = float("%.2f" % wl2) # double
	else:
		wl2 = 0
	
	sql = "INSERT INTO top100 (uid, nickname, kd, kd2, kda, kda2, wr, wr2, wl, wl2, effRating, effRating2, karma, karma2, prestigeBonus, prestigeBonus2, gamePlayed, gamePlayed2, gameWin, gameWin2, totalAssists, totalAssists2, totalBattleTime, totalBattleTime2, totalDeath, totalDeath2, totalDmgDone, totalDmgDone2, totalHealingDone, totalHealingDone2, totalKill, totalKill2, totalVpDmgDone, totalVpDmgDone2, clanName, clanTag) VALUES ('" + str(uid) + "', '" + str(nickname) + "', '" + str(kd) + "', '" + str(kd2) + "', '" + str(kda) + "', '" + str(kda2) + "', '" + str(wr) + "', '" + str(wr2) + "', '" + str(wl) + "', '" + str(wl2) + "', '" + str(effRating) + "', '" + str(effRating2) + "', '" + str(karma) + "', '" + str(karma2) + "', '" + str(prestigeBonus) + "', '" + str(prestigeBonus2) + "', '" + str(gamePlayed) + "', '" + str(gamePlayed2) + "', '" + str(gameWin) + "', '" + str(gameWin2) + "', '" + str(totalAssists) + "', '" + str(totalAssists2) + "', '" + str(totalBattleTime) + "', '" + str(totalBattleTime2) + "', '" + str(totalDeath) + "', '" + str(totalDeath2) + "', '" + str(totalDmgDone) + "', '" + str(totalDmgDone2) + "', '" + str(totalHealingDone) + "', '" + str(totalHealingDone2) + "', '" + str(totalKill) + "', '" + str(totalKill2) + "', '" + str(totalVpDmgDone) + "', '" + str(totalVpDmgDone2) + "', '" + str(clanName) + "', '" + str(clanTag) + "');"
	
	DataBaseRequest(conn, cur, sql)
#end define

def DeleteInTheTop100(uid):
	AddLog("Start DeleteInTheTop100", "debug")
	conn, cur = ConnectToDataBase(mysqlUser, mysqlPass, "sc_history_db")
	sql = "DELETE FROM top100 WHERE uid='" + str(uid) + "'"
	DataBaseRequest(conn, cur, sql)
	DataBaseConnectionClose(conn, cur)
#end define

def GetInformationFromSC(nickname):
	scURL = "http://gmt.star-conflict.com/pubapi/v1/userinfo.php?nickname="
	for i in range(5):
		try:
			webform = (urllib.request.urlopen(scURL + nickname).read()).decode("utf-8")
			webform_json = json.loads(webform)
			return webform_json
		except BaseException as err:
			AddLog("GetInformationFromSC: Attempt: " + str(i) + " " + str(err), "warning")
			sleep(i)
	return None
#end define

def RecordStartTime():
	AddLog("Start RecordStartTime", "debug")
	timestamp = int(time.time())
	conn, cur = ConnectToDataBase(mysqlUser, mysqlPass, "other_db")
	DataBaseRequest(conn, cur, "UPDATE timestamps SET value=" + str(timestamp) + " WHERE nomination='RecordStartTime'")
	DataBaseConnectionClose(conn, cur)
#end define

def RecordEndTime():
	AddLog("Start RecordEndTime", "debug")
	timestamp = int(time.time())
	conn, cur = ConnectToDataBase(mysqlUser, mysqlPass, "other_db")
	DataBaseRequest(conn, cur, "UPDATE timestamps SET value='" + str(timestamp) + "' WHERE nomination='RecordEndTime'")
	DataBaseConnectionClose(conn, cur)
#end define

def AddLog(inputText, mode='info'):
	myName = (sys.argv[0])[:(sys.argv[0]).rfind('.')]
	logName = myName + ".log"
	timeText = time.strftime('%d.%m.%Y, %H:%M:%S'.ljust(20, " "))
	modeText = ('[' + mode + ']').ljust(8, " ")
	logText = timeText + modeText + inputText
	file = open(logName, 'a')
	file.write(logText + "\n")
	file.close()
	
	print(logText)
#end define

def count_lines(filename, chunk_size=1<<13):
	if not os.path.isfile(filename):
		return 0
	with open(filename) as file:
		return sum(chunk.count('\n')
			for chunk in iter(lambda: file.read(chunk_size), ''))
#end define

def chunkIt(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0
	while last < len(seq):
		out.append(seq[int(last):int(last + avg)])
		last += avg
	return out
#end define


###
### Start of the program
###

myName = (sys.argv[0])[:(sys.argv[0]).rfind('.')]
logName = myName + ".log"

if os.path.isfile(logName):
	os.remove(logName)

General()
	


