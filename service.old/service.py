import os
import sys
import time
from time import sleep
import socket
import threading
import MySQLdb # apt-get install libmysqlclient-dev & pip3 install mysqlclient
import gc
import urllib.request
import json


mysqlHost = "localhost"
mysqlUser = "editor"
mysqlPass = "5ohnn0"

host = ''
port = 4800
packetLength = 1024

sock = socket.socket()
sock.bind((host, port))
sock.listen(50)


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

def Main(self):
	buffer = "null"
	while True:
		data = self.conn.recv(packetLength)
		if len(data) < 1:
			return
		try:
			inputText = data.decode('UTF-8').replace("<EOF>", "")
		except UnicodeDecodeError:
			AddLog("The package is not a text", "error")
			return
		AddLog("Get the package: " + inputText, "debug")
		outputText, buffer = Reaction(inputText, buffer)
		
		if outputText != "null":
			bytes = outputText.encode('UTF-8')
			self.conn.send(bytes + b"<EOF>")
#end define

def Reaction(inputText, buffer):
	AddLog("Start Reaction", "debug")
	outputText = 'null'
	if ("<nickname>" in inputText):
		outputText = AddNicknameToMySQL(inputText)
		
	return outputText, buffer
#end define

def AddNicknameToMySQL(inputText):
	AddLog("Start AddNicknameToMySQL", "debug")
	nickname = Parsing(inputText, "<nickname>", "</nickname>")
	
	# Checking the correctness of the nickname
	result = IsNicknameGood(nickname)
	if result < 0:
		return "nickname is not good"
	
	# Check the presence of this nickname in the database
	BDresult, uidFromDB = IsNicknameInMySQL(nickname)
	AddLog("BDresult: " + str(BDresult) + " uidFromDB: " +  str(uidFromDB), "debug");
	
	# Checking the correctness of the nickname through the server SC
	uv_code, uidFromSC = UserVerificationAcrossScApi(nickname)
	AddLog("uv_code: " +  str(uv_code) + " uidFromSC: " +  str(uidFromSC), "debug");
	if uv_code < 0:
		return "user not found"
	
	# Checking whether the nickname is a replacement for the old nickname
	if BDresult > 0:
		if uidFromDB != uidFromSC:
			DeleteRowInTable(nickname)
		else:
			return "user already exists"
	
	# Удалить из lost uids если там есть
	conn, cur = ConnectToDataBase(mysqlUser, mysqlPass, "sc_history_db")
	sql = "DELETE FROM lost_uids WHERE uid='" + str(uidFromSC) + "'"
	row, result = DataBaseRequest(conn, cur, sql)
	DataBaseConnectionClose(conn, cur)
	
	# Добавляем новый ник в БД
	AddLog("New nickname: " + nickname)
	AddEntryIntoTable(uidFromSC, nickname)
	
	return "ok"
#end define

def DeleteRowInTable(nickname):
	AddLog("Start DeleteRowInTable", "debug")
	try:
		conn = MySQLdb.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPass, db="sc_history_db")
	except MySQLdb.Error as err:
		AddLog("Connection error: {}".format(err), "error")
		conn.close()
		
	sql = "DELETE FROM nickname_uid WHERE BINARY nickname='" + nickname + "'"
	
	try:
		cur = conn.cursor(MySQLdb.cursors.DictCursor)
		result = cur.execute(sql)
		data = cur.fetchall()
		conn.commit()
	except MySQLdb.Error as err:
		AddLog("Query error: {}".format(err), "error")
#end define

def IsNicknameGood(nickname):
	"""Проверяем никнейм на нормальность"""
	goodsign_s = "q w e r t y u i o p a s d f g h j k l z x c v b n m Q W E R T Y U I O P A S D F G H J K L Z X C V B N M 1 2 3 4 5 6 7 8 9 0".split(' ')
	user_nikname_0 = list(nickname)
	nickname_cycle = 0
	while nickname_cycle < len(user_nikname_0):
		c_gn_1 = user_nikname_0[nickname_cycle]
		if c_gn_1 not in goodsign_s:
			return -1
		nickname_cycle = nickname_cycle + 1
	return 0
#end define

def UserVerificationAcrossScApi(nickname):
	AddLog('Start UserVerificationAcrossScApi', "debug")
	scURL = 'http://gmt.star-conflict.com/pubapi/v1/userinfo.php?nickname='
	uid = 0
	uv_code = -3 # unknown_error
	if 'empty_result' in nickname:
		uv_code = -2 # Wrong nickname
	else:
		try:
			sleep(0.3)
			webform = (urllib.request.urlopen(scURL + nickname).read(1000)).decode('utf-8')
			json_str = json.loads(webform)
		except:
			AddLog("I'm crying because I can't get a candy ;(", "error")
			return -4, 0
		if json_str['code'] == 1:
			uv_code = -1 # Nickname not found
		elif json_str['code'] == 0:
			uv_code = 0
			serchText = 'uid'
			data = json_str['data']
			if (serchText in data):
				uid = int(data[serchText])
		else:
			AddLog('Error UserVerificationAcrossScApi unknown_error')
	AddLog('UserVerificationAcrossScApi nickname=' + nickname + ' uv_code=' + str(uv_code), "debug")
	return uv_code, uid
# end define

def IsNicknameInMySQL(nickname):
	AddLog('Start IsNicknameInMySQL', "debug")
	result = uid = 0
	
	conn, cur = ConnectToDataBase(mysqlUser, mysqlPass, "sc_history_db")
	
	sql = "SELECT * FROM nickname_uid WHERE BINARY nickname='" + nickname + "'"
	
	row, result = DataBaseRequest(conn, cur, sql)
	AddLog("row: " + str(row), "debug")
	
	DataBaseConnectionClose(conn, cur)
	
	if result > 0:
		uid = row[0]['uid']
	
	return result, uid
#end define

def AddEntryIntoTable(uid, nickname):
	AddLog('Start AddEntryIntoTable', "debug")
	
	conn, cur = ConnectToDataBase(mysqlUser, mysqlPass, "sc_history_db")
	
	sql = "INSERT INTO nickname_uid (uid, nickname) VALUES ('" + str(uid) + "', '" + nickname + "')"
	sql2 = "CREATE TABLE uid_" + str(uid) + " (date DATE, uid  BIGINT, nickname VARCHAR(20), effRating BIGINT, karma BIGINT, prestigeBonus DOUBLE, gamePlayed BIGINT, gameWin BIGINT, totalAssists BIGINT, totalBattleTime BIGINT, totalDeath BIGINT, totalDmgDone BIGINT, totalHealingDone BIGINT, totalKill BIGINT, totalVpDmgDone BIGINT, clanName VARCHAR(20), clanTag VARCHAR(10))"
	
	DataBaseRequest(conn, cur, sql)
	DataBaseRequest(conn, cur, sql2)
	
	DataBaseConnectionClose(conn, cur)
#end define

class Connect(threading.Thread):
	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr
		threading.Thread.__init__(self)
		
	def run (self):
		try:
			Main(self)
			
		except ConnectionResetError:
			AddLog("The client forcibly severed the connection: " + str(self.addr), "error")
			
#end define

def Parsing(inputText, startScan, endScan):
	text_0 = inputText[inputText.find(startScan) + len(startScan):]
	outputText = text_0[:text_0.find(endScan)]
	return outputText
#end define

def HideIpAddress(addr):
	ip = addr[0]
	ip_arr = ip.split('.')
	output = "*.*." + ip_arr[2] + "." + ip_arr[3]
	return output
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
	
	allline = count_lines(logName)
	if (allline > 4096 + 256):
		delline = allline - 4096
		f=open(logName).readlines()
		i = 0
		while i < delline:
			f.pop(0)
			i = i + 1
		with open(logName,'w') as F:
			F.writelines(f)
	print(logText)
#end define

def count_lines(filename, chunk_size=1<<13):
	if not os.path.isfile(filename):
		return 0
	with open(filename) as file:
		return sum(chunk.count('\n')
			for chunk in iter(lambda: file.read(chunk_size), ''))
#end define


###
### Start of the program
###

AddLog('Running the SCHistoryService server on the port: ' + str(port))
while True:
	try:
		sleep(1)
		conn, addr = sock.accept()
		AddLog("--- --- ---")
		AddLog("There is an incoming connection: " + HideIpAddress(addr))
		Connect(conn, addr).start()
	except BaseException as err:
		AddLog("Critical error: " + str(err), "error")
# end while
