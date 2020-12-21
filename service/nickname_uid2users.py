#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import os
import sys
import time
import json
import psutil #pip3 install psutil
import threading
from urllib.request import urlopen
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import VARCHAR
from sqlalchemy.sql import func
from models import *


def Init():
	# Set global variables
	global localdb, localbuffer
	localdb = dict()
	localbuffer = dict()
	

	# Get program, log and database file name
	myName = GetMyName()
	localbuffer["logFileName"] = myName + ".log"
	localbuffer["localdbFileName"] = myName + ".db"

	# First start up
	if not os.path.isfile(localbuffer["localdbFileName"]):
		FirstStartUp()

	# Remove old log file
	if (localdb["isDeleteOldLogFile"] == True and 
		os.path.isfile(localbuffer["logFileName"]) == True):
		os.remove(localbuffer["logFileName"])

	# Logging the start of the program
	AddLog("Start program " + myName)
#end define

def FirstStartUp():
	localdb["isLimitLogFile"] = False
	localdb["isDeleteOldLogFile"] = True
	localdb["logLevel"] = "debug"
	localdb["threadNumber"] = 16 * psutil.cpu_count()
	localdb["mysql"] = dict()
	localdb["mysql"]["host"] = "localhost"
	localdb["mysql"]["user"] = "editor"
	localdb["mysql"]["passwd"] = "9qtrnB5T9P74kNa7"
	localdb["mysql"]["dbName"] = "schistory"
	localdb["mysql"]["limit"] = localdb["threadNumber"] * 300
	localdb["mysql"]["offset"] = 0
	localdb["mysql"]["usingThread"] = list()
	localdb["scURL"] = "http://gmt.star-conflict.com/pubapi/v1/userinfo.php?nickname="

	# Create tables
	engine, session = CreateConnectToDB()
	Base.metadata.create_all(engine)
	CloseDBConnect(engine, session)
#end define

def CreateConnectToDB():
	global localdb
	AddLog("Start CreateConnectToDB function.", "debug")
	# Create MySQL connect
	mysqlConnectUrl = "mysql://{0}:{1}@{2}/{3}".format(localdb["mysql"]["user"], localdb["mysql"]["passwd"], localdb["mysql"]["host"], localdb["mysql"]["dbName"])
	engine = create_engine(mysqlConnectUrl, echo=False)
	Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
	session = Session()
	return engine, session
#end define

def CloseDBConnect(engine, session):
	AddLog("Start CloseDBConnect function.", "debug")
	#try:
	session.flush()
	session.commit()
	#except:
	#	pass
	session.close()
	engine.dispose()
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
	inputText = "{0}".format(inputText)
	myName = GetMyName()
	logName = myName + ".log"
	#timeText = time.strftime("%d.%m.%Y, %H:%M:%S".ljust(21, ' '))
	timeText = DateTimeLibrary.datetime.utcnow().strftime('%d.%m.%Y, %H:%M:%S.%f')[:-3].ljust(27, ' ')

	#pass if set log level
	if (localdb["logLevel"] == "none"):
		return
	elif (localdb["logLevel"] != "debug" and mode == "debug"):
		return

	# set color mode
	if (mode == "info"):
		colorStart = bcolors.INFO + bcolors.BOLD
	elif (mode == "warning"):
		colorStart = bcolors.WARNING + bcolors.BOLD
	elif (mode == "error"):
		colorStart = bcolors.ERROR + bcolors.BOLD
	elif (mode == "debug"):
		colorStart = bcolors.DEBUG + bcolors.BOLD
	else:
		colorStart = bcolors.UNDERLINE + bcolors.BOLD
	modeText = colorStart + ('[' + mode + ']').ljust(10, ' ') + bcolors.ENDC
	
	# set color thread
	if (mode == "error"):
		colorStart = bcolors.ERROR + bcolors.BOLD
	else:
		colorStart = bcolors.OKGREEN + bcolors.BOLD
	threadText = colorStart + ('<' + GetThreadName() + '>').ljust(14, " ") + bcolors.ENDC
	logText = modeText + timeText + threadText + inputText

	# Write log to the file
	file = open(logName, 'a')
	file.write(logText + '\n')
	file.close()

	# Print log text
	print(logText)
	
	# Control log size
	if (localdb["isLimitLogFile"] == False):
		return
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
#end define

def count_lines(filename, chunk_size=1<<13):
	if not os.path.isfile(filename):
		return 0
	with open(filename) as file:
		return sum(chunk.count('\n')
			for chunk in iter(lambda: file.read(chunk_size), ''))
#end define

class bcolors:
	DEBUG = '\033[95m'
	INFO = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	ERROR = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
#end class


def AddUserHistory(**kwargs):
	global session
	uid = kwargs.get("uid")
	nickname = kwargs.get("nickname")
	#clanName = kwargs.get("clanName")
	#clanTag = kwargs.get("clanTag")

	#start = time.time()
	#user = session.query(User).filter_by(uid=uid).first()
	#if not user:
	user = User(uid=uid)
	#else:
	#	AddLog("user '{0}' is already exist!".format(user.uid), "warning")
	#end if
	#end = time.time()
	#over = round(end-start, 2)
	#if (over > 1):
	#	AddLog("query(User) take {0} sec".format(over), "warning")

	#start = time.time()
	#nicknameModel = session.query(Nickname).filter_by(nickname=func.binary(nickname)).first() # nickname=func.binary(nickname)
	#if not nicknameModel:
	nicknameModel = Nickname(nickname=nickname)
	#else:
	#	AddLog("nickname '{0}' is already exist!".format(nickname), "warning")
	#	exit()
	#end if
	#end = time.time()
	#over = round(end-start, 2)
	#if (over > 1):
	#	AddLog("query(Nickname) take {0} sec".format(over), "warning")

	#clan = session.query(Clan).filter_by(name=clanName).first()
	#if not clan:
	#	clan = Clan(name=clanName, tag=clanTag)
	#end if

	#pvp = PVP(gamePlayed=1, gameWin=2, totalAssists=3, totalBattleTime=4, totalDeath=5, totalDmgDone=6, totalHealingDone=7, totalKill=8, totalVpDmgDone=9)
	#pve = PVE(gamePlayed=1)
	#coop = COOP(gamePlayed=1, gameWin=2, totalBattleTime=3)
	#openworld = OpenWorld(karma=1)
	#other = Other(effRating=1, prestigeBonus=2.3, accountRank=4)

	userhistory = UserHistory(userModel=user, nicknameModel=nicknameModel, date=DateTimeLibrary.date.fromtimestamp(0))
	session.add(userhistory)
	#session.commit()
	#AddLog("{0} add".format(nickname))
#end define

def GetDataFromSC(nickname):
	global localdb
	for i in range(1, 4):
		try:
			url = localdb["scURL"] + nickname
			webform = (urlopen(url).read()).decode("utf-8")
			webform_json = json.loads(webform)
			return webform_json
		except BaseException as err:
			AddLog("GetDataFromSC: Attempt: " + str(i) + " " + str(err), "warning")
			time.sleep(i)
	return None
#end define

class Nickname_Uid(Base):
	__tablename__ = 'nickname_uid'

	uid = Column(BIGINT, primary_key=True)
	nickname = Column(VARCHAR(50))
	karma = Column(BIGINT)
	gamePlayed = Column(BIGINT)

	def __repr__(self):
		return '<User_Uid {0}>'.format(self.uid)
	#end define
#end define


###
### Start of the program
###

if __name__ == "__main__":
	Init()
#end if

limit=3000
offset=0
while True:
	engine, session = CreateConnectToDB()

	nickname_uid_list = session.query(Nickname_Uid).limit(limit).offset(offset).all()
	offset+=limit

	if not nickname_uid_list:
		break

	AddLog("start work")
	for nickname_uid in nickname_uid_list:
		nickname = nickname_uid.nickname
		uid = nickname_uid.uid
		AddUserHistory(uid=uid, nickname=nickname)
	#end while



	#users = session.query(User).filter_by(uid=8649247).all()
	#for user in users:
	#	userHistoryList = user.usershistory
	#	nickname = user.GetNickname()
	#	AddLog("item: {0}, {1}".format(nickname, userHistoryList))
	#end for

	CloseDBConnect(engine, session)
#end while
