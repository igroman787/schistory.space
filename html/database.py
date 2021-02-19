#!/usr/bin/env python3
# -*- coding: utf_8 -*-l

import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

class DataBase:
	def __init__(self, user, passwd, db, host):
		self.user = user
		self.passwd = passwd
		self.host = host
		self.db = db
		self.engine = None
		self.session = None
		self.lid = None
	#end define
	
	def CreateConnect(self):
		if self.engine != None and self.session != None:
			return
		# Create MySQL connect
		mysqlConnectUrl = "mysql://{0}:{1}@{2}/{3}".format(self.user, self.passwd, self.host, self.db)
		engine = create_engine(mysqlConnectUrl, echo=False)
		Session = sessionmaker(bind=engine)
		session = Session()
		self.engine = engine
		self.session = session
		self.lid = random.randint(1, 999999)
		return self.lid
	#end define
	
	def CloseConnect(self, lid):
		if self.lid != lid:
			return
		self.session.commit()
		self.session.close()
		self.engine.dispose()
		self.session = None
		self.engine = None
	#end define
	
	def CheckTables(self):
		lid = self.CreateConnect()
		Base.metadata.create_all(self.engine)
		self.session.commit()
		self.CloseConnect(lid)
	#end define
	
	def GetUserHistor(self, uid, limit):
		outputList = list()
		lid = self.CreateConnect()
		historyList = self.session.query(UserHistory).filter_by(uid=uid).order_by(UserHistory.date.desc()).limit(limit).all()
		for h in historyList:
			data = dict()
			# data["uid"] = uid
			data["date"] = h.date.strftime("%Y-%m-%d")
			data["nickname"] = h.nicknameModel.nickname
			data["pvp"] = model2dict(h.pvpModel)
			data["pve"] = model2dict(h.pveModel)
			data["coop"] = model2dict(h.coopModel)
			data["openworld"] = model2dict(h.openworldModel)
			data["other"] = model2dict(h.otherModel)
			data["clan"] = self.GetClan(h.cid, h.date)

			outputList.append(data)
		self.CloseConnect(lid)
		return outputList
	#end define

	def GetUserPassNum(self, uid):
		lid = self.CreateConnect()
		u = self.session.query(User).filter_by(uid=uid).first()
		if u == None:
			return None
		#end if
		pnum = u.pnum
		self.CloseConnect(lid)
		return pnum
	#end define

	def GetClan(self, cid, date):
		outputList = list()
		lid = self.CreateConnect()
		h = self.session.query(ClanHistory).filter_by(cid=cid, date=date).first()
		if h == None:
			return None
		#end if
		
		data = dict()
		# data["cid"] = cid
		data["date"] = h.date.strftime("%Y-%m-%d")
		data["name"] = h.clanNameModel.name
		data["tag"] = h.clanNameModel.tag
		if h.clanRatingModel != None:
			data["pvpRating"] = h.clanRatingModel.pvpRating
			data["pveRating"] = h.clanRatingModel.pveRating
		#end if
		self.CloseConnect(lid)
		return data
	#end define

	def GetLostUids(self, limit):
		outputList = list()
		lid = self.CreateConnect()
		lostuids = self.session.query(LostUid).limit(limit).all()
		for lostuidModel in lostuids:
			outputList.append(lostuidModel.uid)
		self.CloseConnect(lid)
		return outputList
	#end define

	def GetClanHistory(self, cid, limit, getUsers=False):
		outputList = list()
		lid = self.CreateConnect()
		historyList = self.session.query(ClanHistory).filter_by(cid=cid).order_by(ClanHistory.date.desc()).limit(limit).all()
		for h in historyList:
			data = dict()
			# data["cid"] = cid
			data["date"] = h.date.strftime("%Y-%m-%d")
			data["name"] = h.clanNameModel.name
			data["tag"] = h.clanNameModel.tag
			if h.clanRatingModel != None:
				data["pvpRating"] = h.clanRatingModel.pvpRating
				data["pveRating"] = h.clanRatingModel.pveRating
			if getUsers:
				data["uids"] = self.GetClanUsers(cid, date=h.date)
			#end if

			outputList.append(data)
		self.CloseConnect(lid)
		return outputList
	#end define

	def GetClanUsers(self, cid, date):
		outputList = list()
		lid = self.CreateConnect()
		historyList = self.session.query(UserHistory).filter_by(cid=cid, date=date).all()
		for clanHistoryModel in historyList:
			outputList.append(clanHistoryModel.uid)
		self.CloseConnect(lid)
		return outputList
	#end define

	def GetFromList(self, inputList, i):
		try:
			return inputList[i]
		except IndexError:
			return None
	#end define

	def GetTableStatus(self, tableName):
		lid = self.CreateConnect()
		result = self.engine.execute("SHOW TABLE STATUS LIKE '{tableName}'".format(tableName=tableName))
		data = result.fetchone()
		self.CloseConnect(lid)
		return data
	#end define

	def GetTimes(self):
		lid = self.CreateConnect()
		q1 = self.session.query(DataBaseUpdateTime).filter_by(name="startDataBaseUpdateTime").first()
		q2 = self.session.query(DataBaseUpdateTime).filter_by(name="endDataBaseUpdateTime").first()
		if q1 == None or q2 == None:
			return None
		#end if

		data = dict()
		data["startDataBaseUpdateTime"] = q1.datetime.strftime("%Y-%m-%d %H:%M:%S")
		data["endDataBaseUpdateTime"] = q2.datetime.strftime("%Y-%m-%d %H:%M:%S")
		self.CloseConnect(lid)
		return data
	#end define
#end class
