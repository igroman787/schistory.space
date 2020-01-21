#!/usr/bin/env python3
# -*- coding: utf_8 -*-

'''
This module is intended for a single DB update - saving the history of SC pilots
It should be used through cron, for example: @daily /usr/bin/python3 /etc/schistory/updateDatabase.py
Before starting this script run the following steps:
1. Install:
	apt-get install mysql-server mysql-client libmysqlclient-dev
	pip3 install psutil mysqlclient sqlalchemy
2. Create user and DB in MySQL
	CREATE USER 'editor'@'localhost' IDENTIFIED BY 'passwd44c4';
	GRANT ALL PRIVILEGES ON schistory.* TO 'editor'@'localhost';
	CREATE DATABASE schistory;
3. Restore DB:
	wget https://raw.githubusercontent.com/igroman787/schistory.space/master/schistory.sql.zip
	unzip schistory.sql.zip
	mysql schistory < schistory.sql
'''

import os
import sys
import time
import json
import fcntl
import psutil
import threading
from urllib.request import urlopen
import datetime as DateTimeLibrary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func, select
from models import *


def Init():
	# Set global variables
	global localdb, localbuffer
	localdb = dict()
	localbuffer = dict()
	localbuffer["logList"] = list()
	localbuffer["cidList"] = list()
	localbuffer["clanList"] = list()
	localbuffer["selfTestingResult"] = dict()
	localbuffer["mysqlOffset"] = 0

	# Get program, log and database file name
	myName = GetMyName()
	myPath = GetMyPath()
	localbuffer["logFileName"] = myName + ".log"
	localbuffer["localdbFileName"] = myName + ".db"
	localbuffer["lockFileName"] = myPath + '.' + myName + ".lock"

	# Start only one process (exit if process exist)
	StartOnlyOneProcess()

	# Start other threads
	threading.Thread(target=Logging, name="Logging", daemon=True).start()
	threading.Thread(target=SelfTesting, name="SelfTesting", daemon=True).start()

	# First start up
	if not os.path.isfile(localbuffer["localdbFileName"]):
		FirstStartUp()

	# Remove old log file
	if (localdb["isDeleteOldLogFile"] == True and os.path.isfile(localbuffer["logFileName"]) == True):
		os.remove(localbuffer["logFileName"])

	# Logging the start of the program
	AddLog("Start program \"{0}\"".format(GetMyFullPath()))

	# Create all tables
	engine, session = CreateConnectToDB()
	Base.metadata.create_all(engine)
	CloseDBConnect(engine, session)
#end define

def StartOnlyOneProcess():
	myName = GetMyName()
	myPath = GetMyPath()
	lockFileName = localbuffer["lockFileName"]
	if os.path.isfile(lockFileName):
		file = open(lockFileName, 'r')
		pid_str = file.read()
		file.close()
		try:
			pid = int(pid_str)
			process = psutil.Process(pid)
			fullProcessName = " ".join(process.cmdline())
		except:
			fullProcessName = ""
		if (fullProcessName.find(GetMyFullName()) > -1):
			print("The process is already running")
			sys.exit(0)
		else:
			WritePidToLockFile()
	else:
		WritePidToLockFile()
#end define

def WritePidToLockFile():
	pid = os.getpid()
	pid_str = str(pid)
	lockFileName = localbuffer["lockFileName"]
	file = open(lockFileName, 'w')
	file.write(pid_str)
	file.close()
#end define

def DeleteLockFile():
	lockFileName = localbuffer["lockFileName"]
	os.remove(lockFileName)
#end define

def FirstStartUp():
	global localdb
	### fix me! ###
	localdb["isLimitLogFile"] = False
	localdb["isDeleteOldLogFile"] = True
	localdb["logLevel"] = "info" # info || debug
	localdb["isIgnorLogWarning"] = False
	localdb["threadNumber"] = 16 * psutil.cpu_count()
	localdb["mysql"] = dict()
	localdb["mysql"]["host"] = "localhost"
	localdb["mysql"]["user"] = "editor"
	localdb["mysql"]["passwd"] = "passwd44c4"
	localdb["mysql"]["dbName"] = "schistory"
	localdb["mysql"]["limit"] = 300
	localdb["mysql"]["usingThread"] = list()
	localdb["scURL"] = "http://gmt.star-conflict.com/pubapi/v1/userinfo.php?nickname="
	localdb["memoryUsinglimit"] = 450
	### fix me! ###
#end define

def General():
	global localdb
	AddLog("Start General function.", "debug")
	RecordStartTime()

	# Remember the number of users
	localbuffer["usersLen"] = GetCountOfUsers()

	# Hand out work
	localbuffer["selfTestingResult"]["threadCountOld"] = threading.active_count()
	for i in range(localdb["threadNumber"]):
		threading.Thread(target=TryScanInformation).start()

	# Wait for the end of work
	while True:
		time.sleep(60)
		PrintSelfTestingResult()
		if localbuffer["selfTestingResult"]["threadCountOld"] == localbuffer["selfTestingResult"]["threadCount"]:
			break
	#end while

	# Write clans to DB
	SaveClansToDB()

	# Check DB
	CheckDB()

	RecordEndTime()
#end define

def GetCountOfUsers():
	engine, session = CreateConnectToDB()
	result = session.query(User).count()
	CloseDBConnect(engine, session)
	return result
#end define

def RecordStartTime():
	localbuffer["start"] = int(time.time())
	localbuffer["usersSavedLen"] = 0

	# Create MySQL connect
	engine, session = CreateConnectToDB()

	# Get module from DB
	timeName = "startDataBaseUpdateTime"
	updateTime = session.query(DataBaseUpdateTime).filter_by(name=timeName).first()
	if not updateTime:
		updateTime = DataBaseUpdateTime(name=timeName)
		session.add(updateTime)
	#end if

	# Update datetime
	updateTime.datetime = DateTimeLibrary.datetime.utcnow()

	# Close DB connect
	CloseDBConnect(engine, session)
#end define

def RecordEndTime():
	global localdb
	end = int(time.time())
	total = end - localbuffer["start"]
	ups = int(localbuffer["usersSavedLen"]/total)
	AddLog("Total time: {0}sec. Total users: {1}".format(total, localbuffer["usersSavedLen"]))
	AddLog("{0}ups (user per second). Total threads: {1}".format(ups, localdb["threadNumber"]))

	# Create MySQL connect
	engine, session = CreateConnectToDB()

	# Get module from DB
	timeName = "endDataBaseUpdateTime"
	updateTime = session.query(DataBaseUpdateTime).filter_by(name=timeName).first()
	if not updateTime:
		updateTime = DataBaseUpdateTime(name=timeName)
		session.add(updateTime)
	#end if

	# Update datetime
	updateTime.datetime = DateTimeLibrary.datetime.utcnow()

	# Close DB connection
	CloseDBConnect(engine, session)
#end define

def TryScanInformation():
	try:
		ScanInformation()
	except Exception as err:
		AddLog("TryScanInformation: {0}".format(err), "error")
		GiveDBConnect()
#end define

def ScanInformation():
	global localdb
	AddLog("Start ScanInformation function.", "debug")

	while True:
		# Create MySQL connect
		engine, session = CreateConnectToDB()

		# Get data from DB
		TakeDBConnect()
		limit = localdb["mysql"]["limit"]
		offset = localbuffer["mysqlOffset"]
		start = time.time()
		partOfUsersList = session.query(User).limit(limit).offset(offset).all()
		localbuffer["mysqlOffset"] += limit
		end = time.time()
		over = round(end-start, 2)
		if over > 1:
			AddLog("ScanInformation(session.query) take {0} sec".format(over), "warning")
		GiveDBConnect()

		# Scan users
		for user in partOfUsersList:
			TryScanUser(user=user, session=session)
		#end for

		# Close DB connection
		CloseDBConnect(engine, session)

		# Break if users end
		if len(partOfUsersList) == 0:
			break
	#end while
#end define

def TryScanUser(**args):
	try:
		user = args.get("user")
		session = args.get("session")
		ScanUser(user=user, session=session)
	except Exception as err:
		AddLog("TryScanUser: {0}".format(err), "error")
#end define

def ScanUser(**args):
	user = args.get("user")
	session = args.get("session")
	uid = user.uid
	nickname = user.GetNickname()
	AddLog("Start ScanUser function. nickname: {0}. uid: {1}".format(nickname, uid), "debug")

	localbuffer["usersSavedLen"] += 1
	webform_json = GetDataFromSC(nickname)

	# If all is bad
	if webform_json == None:
		AddLog("I'm crying because I can't get a candy ;(", "error")

	elif len(nickname) > 20:
		AddLog("Bad nickname: {0}".format(nickname), "warning")

	# If invalid nickname
	elif webform_json["code"] == 1:
		AddLog("Invalid nickname: {0}".format(nickname), "debug")
		RememberLostUid(uid)

	# If everything is ok
	elif webform_json["code"] == 0:
		data = webform_json["data"]
		PrepareDataForWriteInDB(user=user, nickname=nickname, data=data, session=session)
#end define

def PrepareDataForWriteInDB(**args):
	user = args.get("user")
	nickname = args.get("nickname")
	data = args.get("data")
	session = args.get("session")
	uid = user.uid
	AddLog("Start PrepareDataForWriteInDB function. nickname: {0}. uid: {1}".format(nickname, uid), "debug")

	# Check if uid is correct
	if uid != data.get("uid"):
		AddLog("PrepareDataForWriteInDB: uid from DB {0} doesn't coincide with uid from SC {1}".format(uid, data.get("uid")), "warning")
		RememberLostUid(uid)
		return
	#end if

	# Other
	newNickname = GetDataFromJson(data, "nickName")
	effRating = GetDataFromJson(data, "effRating", "int")
	prestigeBonus = GetDataFromJson(data, "prestigeBonus", "float")
	accountRank = GetDataFromJson(data, "accountRank", "int")

	# Pvp
	pvp = GetDataFromJson(data, "pvp")
	pvpGamePlayed = GetDataFromJson(pvp, "gamePlayed", "int")
	pvpGameWin = GetDataFromJson(pvp, "gameWin", "int")
	pvpTotalAssists = GetDataFromJson(pvp, "totalAssists", "int")
	pvpTotalBattleTime = GetDataFromJson(pvp, "totalBattleTime", "int")
	pvpTotalDeath = GetDataFromJson(pvp, "totalDeath", "int")
	pvpTotalDmgDone = GetDataFromJson(pvp, "totalDmgDone", "int")
	pvpTotalHealingDone = GetDataFromJson(pvp, "totalHealingDone", "int")
	pvpTotalKill = GetDataFromJson(pvp, "totalKill", "int")
	pvpTotalVpDmgDone = GetDataFromJson(pvp, "totalVpDmgDone", "int")

	# Pve
	pve = GetDataFromJson(data, "pve")
	pveGamePlayed = GetDataFromJson(pve, "gamePlayed", "int")

	# Coop
	coop = GetDataFromJson(data, "coop")
	coopGamePlayed = GetDataFromJson(coop, "gamePlayed", "int")
	coopGameWin = GetDataFromJson(coop, "gameWin", "int")
	coopTotalBattleTime = GetDataFromJson(coop, "totalBattleTime", "int")

	# OpenWorld
	openWorld = GetDataFromJson(data, "openWorld")
	openWorldKarma = GetDataFromJson(openWorld, "karma")

	# Clan
	clan = GetDataFromJson(data, "clan")
	cid = GetDataFromJson(clan, "cid")
	clanName = GetDataFromJson(clan, "name")
	clanTag = GetDataFromJson(clan, "tag")
	clanPvpRating = GetDataFromJson(clan, "pvpRating")
	clanPveRating = GetDataFromJson(clan, "pveRating")

	# Create user model
	userModel = session.query(User).filter_by(uid=uid).first()
	pvpModel = None
	pveModel = None
	coopModel = None
	openWorldModel = None
	otherModel = None

	# Create nickname model
	if newNickname != nickname:
		nickname = newNickname
		nicknameModel = Nickname(nickname=nickname)
	else:
		nicknameModel = userModel.GetNicknameModel()
	#end if

	# Create PVP model
	if pvp:
		pvpModel = userModel.GetPvpModel()
		if not pvpModel or pvpModel.gamePlayed != pvpGamePlayed:
			pvpModel = PVP(gamePlayed=pvpGamePlayed, gameWin=pvpGameWin, totalAssists=pvpTotalAssists, totalBattleTime=pvpTotalBattleTime, totalDeath=pvpTotalDeath, totalDmgDone=pvpTotalDmgDone,
				totalHealingDone=pvpTotalHealingDone, totalKill=pvpTotalKill, totalVpDmgDone=pvpTotalVpDmgDone)
		#end if
	#end if

	# Create PVE model
	if pve:
		pveModel = userModel.GetPveModel()
		if not pveModel or pveModel.gamePlayed != pveGamePlayed:
			pveModel = PVE(gamePlayed=pveGamePlayed)
		#end if
	#end if

	# Create COOP model
	if coop:
		coopModel = userModel.GetCoopModel()
		if not coopModel or coopModel.gamePlayed != coopGamePlayed:
			coopModel = COOP(gamePlayed=coopGamePlayed, gameWin=coopGameWin, totalBattleTime=coopTotalBattleTime)
		#end if
	#end if

	# Create OpenWorld model
	if openWorld:
		openWorldModel = userModel.GetOpenWorldModel()
		if not openWorldModel or openWorldModel.karma != openWorldKarma:
			openWorldModel = OpenWorld(karma=openWorldKarma)
		#end if
	#end if

	# Create Other model
	if effRating or prestigeBonus or accountRank:
		otherModel = userModel.GetOtherModel()
		if not otherModel or otherModel.effRating != effRating or otherModel.prestigeBonus != prestigeBonus or otherModel.accountRank != accountRank:
			otherModel = Other(effRating=effRating, prestigeBonus=prestigeBonus, accountRank=accountRank)
		#end if
	#end if

	# Create User History model
	userHistoryModel = UserHistory(userModel=userModel, nicknameModel=nicknameModel, pvpModel=pvpModel, pveModel=pveModel, coopModel=coopModel, openworldModel=openWorldModel,
		otherModel=otherModel, cid=cid)
	session.add(userHistoryModel)

	# Add clan to list
	AddClan(cid=cid, clanName=clanName, clanTag=clanTag, clanPvpRating=clanPvpRating, clanPveRating=clanPveRating)

	# Write User History model to DB
	AddLog("Start WriteInDB function. nickname: {0}. uid: {1}".format(nickname, uid), "debug")
#end define

def RememberLostUid(uid):
	AddLog("Start RememberLostUid function. uid: {0}".format(uid), "debug")

	# Create MySQL connect
	engine, session = CreateConnectToDB()

	# Get module from DB
	lostUid = session.query(LostUid).filter_by(uid=uid).first()
	if not lostUid:
		lostUid = LostUid(uid=uid)
		session.add(lostUid)
	#end if

	# Close DB connection
	CloseDBConnect(engine, session)
#end define

def AddClan(**args):
	cid = args.get("cid")
	if cid not in localbuffer["cidList"]:
		localbuffer["cidList"].append(cid)
		localbuffer["clanList"].append(args)
#end define

def SaveClansToDB():
	# Create MySQL connect
	engine, session = CreateConnectToDB()

	for item in localbuffer["clanList"]:
		item["session"] = session
		WriteClanToDB(item)
	#end for

	# Close DB connect
	CloseDBConnect(engine, session)
#end define

def WriteClanToDB(args):
	session = args.get("session")
	cid = args.get("cid")
	clanName = args.get("clanName")
	clanTag = args.get("clanTag")
	clanPvpRating = args.get("clanPvpRating")
	clanPveRating = args.get("clanPveRating")

	# Create Clan model
	clanModel = session.query(Clan).filter_by(cid=cid).first()
	if not clanModel and cid:
		clanModel = Clan(cid=cid)
	#end if

	# Create clanname model
	if clanModel:
		clanNameModel = clanModel.GetClanNameModel()
		if not clanNameModel or clanNameModel.name != clanName or clanNameModel.tag != clanTag:
			clanNameModel = ClanName(name=clanName, tag=clanTag)
		#end if
	#end if

	# Create Clan Rating model
	if clanModel:
		clanRatingModel = clanModel.GetClanRatingModel()
		if not clanRatingModel or clanRatingModel.pvpRating != clanPvpRating or clanRatingModel.pveRating != clanPveRating:
			clanRatingModel = ClanRating(pvpRating=clanPvpRating, pveRating=clanPveRating)
		#end if
	#end if

	# Create Clan History model
	if clanModel:
		clanHistoryModel = ClanHistory(clanModel=clanModel, clanNameModel=clanNameModel, clanRatingModel=clanRatingModel)
		session.add(clanHistoryModel)
	#end if
#end define

def CheckDB():
	AddLog("Start CheckDB function.", "debug")
	# Create MySQL connetion
	engine, session = CreateConnectToDB()
	conn = engine.connect()

	s = SelectHaving(Nickname.nickname)
	result = conn.execute(s)
	if result.rowcount > 0:
		AddLog("Table nicknames - {0}warning{1}: Found {2} matches".format(bcolors.WARNING, bcolors.ENDC, result.rowcount), "warning")
	else:
		AddLog("Table nicknames - {0}OK{1}".format(bcolors.OKGREEN, bcolors.ENDC))
	#end if

	s = SelectHaving(ClanName.name)
	result = conn.execute(s)
	if result.rowcount > 0:
		AddLog("Table clannames - {0}warning{1}: Found {2} matches".format(bcolors.WARNING, bcolors.ENDC, result.rowcount), "warning")
	else:
		AddLog("Table clannames - {0}OK{1}".format(bcolors.OKGREEN, bcolors.ENDC))
	#end if

	conn.close()
	CloseDBConnect(engine, session)
#end define

def SelectHaving(var):
	return select([var,func.count(var)]).group_by(var).having(func.count(var)>1)
#end define

def GetDataFromJson(inputData, serchText, outputDataTypeString="default"):
	outputData = None
	if inputData != None and serchText in inputData:
		if outputDataTypeString == "default":
			outputData = inputData[serchText]
		elif outputDataTypeString == "int":
			outputData = int(inputData[serchText])
		elif outputDataTypeString == "float":
			outputData = float(inputData[serchText])
	return outputData
#end define

def CreateConnectToDB():
	global localdb
	AddLog("Start CreateConnectToDB function.", "debug")
	# Create MySQL connect
	mysqlConnectUrl = "mysql://{0}:{1}@{2}/{3}".format(localdb["mysql"]["user"], localdb["mysql"]["passwd"], localdb["mysql"]["host"], localdb["mysql"]["dbName"])
	engine = create_engine(mysqlConnectUrl, echo=False)
	Session = sessionmaker(bind=engine)
	session = Session()
	return engine, session
#end define

def CloseDBConnect(engine, session):
	start = time.time()
	session.commit()
	session.close()
	engine.dispose()
	end = time.time()
	over = round(end-start, 2)
	if over > 1:
		AddLog("CloseDBConnect take {0} sec".format(over), "warning")
#end define

def TakeDBConnect():
	global localdb
	while True:
		if len(localdb["mysql"]["usingThread"]) > 0:
			time.sleep(0.1)
		else:
			localdb["mysql"]["usingThread"].append(GetThreadName())
			break
#end define

def GiveDBConnect():
	global localdb
	threadName = GetThreadName()
	if threadName in localdb["mysql"]["usingThread"]:
		localdb["mysql"]["usingThread"].remove(threadName)
#end define

def GetDataFromSC(nickname):
	global localdb
	start = time.time()
	outputData = None
	for i in range(1, 4):
		try:
			url = localdb["scURL"] + nickname
			webform = (urlopen(url).read()).decode("utf-8")
			outputData = json.loads(webform)
			break
		except BaseException as err:
			AddLog("GetDataFromSC: Attempt: " + str(i) + " " + str(err), "warning")
			time.sleep(i)
	#end for
	end = time.time()
	over = round(end-start, 2)
	if over > 1:
		AddLog("GetDataFromSC({0}) take {1} sec".format(nickname, over), "warning")
	return outputData
#end define

def SelfTesting():
	while True:
		try:
			time.sleep(1)
			SelfTest()
		except Exception as err:
			AddLog("SelfTesting: {0}".format(err), "error")
#end define

def SelfTest():
	process = psutil.Process(os.getpid())
	memoryUsing = int(process.memory_info().rss/1024/1024)
	threadCount = threading.active_count()
	localbuffer["selfTestingResult"]["memoryUsing"] = memoryUsing
	localbuffer["selfTestingResult"]["threadCount"] = threadCount
	if memoryUsing > localdb["memoryUsinglimit"]:
		localdb["memoryUsinglimit"] += 50
		AddLog("Memory using: {0}Mb".format(memoryUsing), "warning")
#end define

def PrintSelfTestingResult():
	threadCount_old = localbuffer["selfTestingResult"]["threadCountOld"]
	threadCount_new = localbuffer["selfTestingResult"]["threadCount"]
	memoryUsing = localbuffer["selfTestingResult"]["memoryUsing"]
	usersSavedLen = localbuffer["usersSavedLen"]
	usersLen = localbuffer["usersLen"]
	usersSavedPercent = round(usersSavedLen/usersLen*100, 1)
	timestamp = int(time.time())
	timePassed = timestamp - localbuffer["start"]
	timeLeft = int((usersLen - usersSavedLen)/(usersSavedLen/timePassed))
	finishedTime = time.strftime("%d.%m.%Y, %H:%M:%S", time.gmtime(timestamp+timeLeft))
	AddLog("{0}Self testing informatinon:{1}".format(bcolors.INFO, bcolors.ENDC))
	AddLog("Threads: {0} -> {1}".format(threadCount_new, threadCount_old))
	AddLog("Memory using: {0}Mb".format(memoryUsing))
	AddLog("Users: {0} -> {1} ({2}%)".format(usersSavedLen, usersLen, usersSavedPercent))
	AddLog("Time passed: {0} sec. Time left: {1} sec. Will be finished: {2} (UTC)".format(timePassed, timeLeft, finishedTime))
#end define

def GetThreadName():
	return threading.currentThread().getName()
#end define

def GetMyFullName():
	myFullName = sys.argv[0]
	return myFullName
#end define

def GetMyName():
	myFullName = GetMyFullName()
	myName = myFullName[:myFullName.rfind('.')]
	return myName
#end define

def GetMyFullPath():
	myFullName = GetMyFullName()
	myFullPath = os.path.abspath(myFullName)
	return myFullPath
#end define

def GetMyPath():
	myFullPath = GetMyFullPath()
	myPath = myFullPath[:myFullPath.rfind('/')+1]
	return myPath
#end define

def AddLog(inputText, mode="info"):
	global localdb
	inputText = "{0}".format(inputText)
	timeText = DateTimeLibrary.datetime.utcnow().strftime("%d.%m.%Y, %H:%M:%S.%f")[:-3]
	timeText = "{0} (UTC)".format(timeText).ljust(32, ' ')

	# Pass if set log level
	if localdb["logLevel"] != "debug" and mode == "debug":
		return
	elif localdb["isIgnorLogWarning"] == True and mode == "warning":
		return

	# Set color mode
	if mode == "info":
		colorStart = bcolors.INFO + bcolors.BOLD
	elif mode == "warning":
		colorStart = bcolors.WARNING + bcolors.BOLD
	elif mode == "error":
		colorStart = bcolors.ERROR + bcolors.BOLD
	elif mode == "debug":
		colorStart = bcolors.DEBUG + bcolors.BOLD
	else:
		colorStart = bcolors.UNDERLINE + bcolors.BOLD
	modeText = "{0}{1}{2}".format(colorStart, "[{0}]".format(mode).ljust(10, ' '), bcolors.ENDC)

	# Set color thread
	if mode == "error":
		colorStart = bcolors.ERROR + bcolors.BOLD
	else:
		colorStart = bcolors.OKGREEN + bcolors.BOLD
	threadText = "{0}{1}{2}".format(colorStart, "<{0}>".format(GetThreadName()).ljust(14, ' '), bcolors.ENDC)
	logText = modeText + timeText + threadText + inputText

	# Queue for recording
	localbuffer["logList"].append(logText)

	# Print log text
	print(logText)
#end define

def Logging():
	while True:
		time.sleep(1)
		TryWriteLogFile()
#end define

def TryWriteLogFile():
	try:
		WriteLogFile()
	except Exception as err:
		AddLog("TryWriteLogFile: {0}".format(err), "error")
#end define

def WriteLogFile():
	logName = localbuffer["logFileName"]

	file = open(logName, 'a')
	while len(localbuffer["logList"]) > 0:
		logText = localbuffer["logList"].pop(0)
		file.write(logText + '\n')
	#end for
	file.close()

	# Control log size
	if localdb["isLimitLogFile"] == False:
		return
	allline = count_lines(logName)
	if allline > 4096 + 256:
		delline = allline - 4096
		f=open(logName).readlines()
		i = 0
		while i < delline:
			f.pop(0)
			i = i + 1
		with open(logName,'w') as F:
			F.writelines(f)
#end define

def count_lines(filename, chunk_size=1<<13):
	if not os.path.isfile(filename):
		return 0
	with open(filename) as file:
		return sum(chunk.count('\n')
			for chunk in iter(lambda: file.read(chunk_size), ''))
#end define

def CorrectExit():
	time.sleep(1.1)
	DeleteLockFile()
#end define

class bcolors:
	'''This class is designed to display text in color format'''
	DEBUG = '\033[95m'
	INFO = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	ERROR = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
#end class


###
### Start of the program
###

if __name__ == "__main__":
	Init()
	General()
	CorrectExit()
#end if
