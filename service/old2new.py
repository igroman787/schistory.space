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
from updateDatabase import *
import MySQLdb

localbuffer = dict()
localbuffer["logList"] = list()
localbuffer["cidList"] = list()
localbuffer["clanList"] = list()
localbuffer["selfTestingResult"] = dict()
localbuffer["mysqlOffset"] = 0

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

def ConnectToDataBase(user, passwd, db):
	try:
		conn = MySQLdb.connect(host="localhost", user=user, passwd=passwd, db=db)
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
		AddLog("DataBaseRequest: " + str(err), "warning")
		AddLog("DataBaseRequest: " + sql, "debug")
		result = -1 * err.args[0]
		return None, result
#end define

def DataBaseConnectionClose(conn, cur):
	cur.close()
	conn.close()
#end define

def AddUserHistory(**kwargs):
	uid = kwargs.get("uid")
	data = kwargs.get("data")
	session = kwargs.get("session")

	date = data.get("date")
	nickname = data.get("nickname")
	effRating = data.get("effRating")
	karma = data.get("karma")
	prestigeBonus = data.get("prestigeBonus")
	gamePlayed = data.get("gamePlayed")
	gameWin = data.get("gameWin")
	totalAssists = data.get("totalAssists")
	totalBattleTime = data.get("totalBattleTime")
	totalDeath = data.get("totalDeath")
	totalDmgDone = data.get("totalDmgDone")
	totalHealingDone = data.get("totalHealingDone")
	totalKill = data.get("totalKill")
	totalVpDmgDone = data.get("totalVpDmgDone")
	clanName = data.get("clanName")
	clanTag = data.get("clanTag")
	

	userModel = session.query(User).filter_by(uid=uid).first()
	if not userModel:
		userModel = User(uid=uid)
	#end if

	#nicknameModel = session.query(Nickname).filter_by(nickname=nickname).first()
	#if not nicknameModel:
	#	nicknameModel = Nickname(nickname=nickname)
	#end if

	try:
		nicknameModel = userModel.GetNicknameModel()
	except:
		nicknameModel = Nickname(nickname=nickname)
	#end if

	pvpModel = userModel.GetPvpModel()
	if not pvpModel or pvpModel.gamePlayed != gamePlayed:
		pvpModel = PVP(gamePlayed=gamePlayed, gameWin=gameWin, totalAssists=totalAssists, totalBattleTime=totalBattleTime, totalDeath=totalDeath, totalDmgDone=totalDmgDone,
			totalHealingDone=totalHealingDone, totalKill=totalKill, totalVpDmgDone=totalVpDmgDone)
	#end if

	openworldModel = userModel.GetOpenWorldModel()
	if not openworldModel or openworldModel.karma != karma:
		openworldModel = OpenWorld(karma=karma)
	#end if
	
	otherModel = userModel.GetOtherModel()
	if not otherModel or otherModel.effRating != effRating or otherModel.prestigeBonus != prestigeBonus:
		otherModel = Other(effRating=effRating, prestigeBonus=prestigeBonus)
	#end if

	cid = None
	if clanName:
		#AddClan(cid=cid, clanName=clanName, clanTag=clanTag)
		# Create Clan model
		clanNameModel = session.query(ClanName).filter_by(name=clanName, tag=clanTag).first()
		cid = clanNameModel.clanHistoryModel[-1].clanModel.cid
		AddClan_new(cid=cid, clanName=clanName, clanTag=clanTag, date=date, session=session)
		
	#end if

	userhistory = UserHistory(userModel=userModel, nicknameModel=nicknameModel, date=date, cid=cid, pvpModel=pvpModel, openworldModel=openworldModel, otherModel=otherModel)
	session.add(userhistory)
#end define

def AddClan(**args):
	cid = args.get("cid")
	if cid not in localbuffer["cidList"]:
		localbuffer["cidList"].append(cid)
		localbuffer["clanList"].append(args)
#end define

def AddClan_new(**args):
	cid = args.get("cid")
	clanName = args.get("clanName")
	clanTag = args.get("clanTag")
	date = args.get("date")
	session = args.get("session")

	#engine, session = CreateConnectToDB()

	clanModel = session.query(Clan).filter_by(cid=cid).first()

	# Create clanname model
	if clanModel:
		clanNameModel = clanModel.GetClanNameModel()
		if not clanNameModel or clanNameModel.name != clanName or clanNameModel.tag != clanTag:
			clanNameModel = ClanName(name=clanName, tag=clanTag)
		#end if
	#end if

	# Create Clan History model
	if clanModel:
		clanHistoryModel = ClanHistory(clanModel=clanModel, clanNameModel=clanNameModel, date=date)
		session.add(clanHistoryModel)
	#end if

	#CloseDBConnect(engine, session)
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
	global cid
	session = args.get("session")
	clanName = args.get("clanName")
	clanTag = args.get("clanTag")
	clanModel = None

	# Create Clan model
	clanNameModel = session.query(ClanName).filter_by(name=clanName).first()
	if clanNameModel and clanNameModel.clanHistoryModel:
		clanModel = session.query(Clan).filter_by(cid=clanNameModel.clanHistoryModel[-1].clanModel.cid).first()
	if not clanModel:
		clanModel = Clan(cid=cid)
	#end if

	# Create clanname model
	if clanModel:
		clanNameModel = clanModel.GetClanNameModel()
		if not clanNameModel or clanNameModel.name != clanName or clanNameModel.tag != clanTag:
			clanNameModel = ClanName(name=clanName, tag=clanTag)
		#end if
	#end if

	# Create Clan History model
	if clanModel:
		clanHistoryModel = ClanHistory(clanModel=clanModel, clanNameModel=clanNameModel)
		session.add(clanHistoryModel)
	#end if
#end define

def P2():
	global limit, offset
	while True:
		engine, session = CreateConnectToDB()
		conn, cur = ConnectToDataBase("editor", "9qtrnB5T9P74kNa7", "sc_history_db")

		TakeDBConnect()
		nickname_uid_list = session.query(Nickname_Uid).limit(limit).offset(offset).all()
		offset+=limit
		GiveDBConnect()

		if not nickname_uid_list:
			AddLog("no work")
			break

		AddLog("start work")
		for nickname_uid in nickname_uid_list:
			row, result = DataBaseRequest(conn, cur, "select * from uid_{0} ORDER BY date DESC".format(nickname_uid.uid))
			if result < 1:
				continue
			#end if

			for item in row:
				AddUserHistory(uid=nickname_uid.uid, data=item, session=session)
			AddLog("{0} added".format(nickname_uid.nickname))
		#end while

		DataBaseConnectionClose(conn, cur)
		CloseDBConnect(engine, session)
	#end while
#end define


###
### Start of the program
###

if __name__ == "__main__":
	Init()
#end if

limit=300
offset=0

P2()


AddLog("Done")