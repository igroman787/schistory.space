#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, cast, Column, ForeignKey, String, SMALLINT, BIGINT, INT, FLOAT, DATE, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship, foreign, remote
import datetime as DateTimeLibrary
from sqlalchemy.ext.declarative import DeclarativeMeta


# SQLAlchemy init
Base = declarative_base()

class DataBaseUpdateTime(Base):
	__tablename__ = "times"
	id = Column(INT, primary_key=True)
	name = Column(String(64, collation="utf8_bin"), unique=True)
	datetime = Column(DateTime)

	def __repr__(self):
		return "<Time {}>".format(self.startUpdateDataBaseTime)
	#end define
#end class

class LostUid(Base):
	__tablename__ = "lostuids"
	id = Column(INT, primary_key=True)
	uid = Column(INT, index=True, unique=True)

	def __repr__(self):
		return "<LostUid {}>".format(self.uid)
	#end define
#end class

class User(Base):
	__tablename__ = "users"

	uid = Column(INT, primary_key=True)
	pnum = Column(TINYINT, default=0)

	userhistoryModel = relationship("UserHistory", primaryjoin="remote(UserHistory.uid) == foreign(User.uid)", uselist=True)

	def __repr__(self):
		return "<User {0}>".format(self.uid)
	#end define

	def GetNickname(self):
		return self.userhistoryModel[-1].nicknameModel.nickname
	#end define

	def GetNicknameModel(self):
		return self.userhistoryModel[-1].nicknameModel
	#end define

	def GetClanId(self):
		return self.userhistoryModel[-1].cid
	#end define

	def GetPvpModel(self):
		return self.userhistoryModel[-1].pvpModel
	#end define

	def GetPveModel(self):
		return self.userhistoryModel[-1].pveModel
	#end define

	def GetCoopModel(self):
		return self.userhistoryModel[-1].coopModel
	#end define

	def GetOpenWorldModel(self):
		return self.userhistoryModel[-1].openworldModel
	#end define

	def GetOtherModel(self):
		return self.userhistoryModel[-1].otherModel
	#end define
#end class

class UserHistory(Base):
	__tablename__ = "usershistory"

	uhid = Column(BIGINT, primary_key=True)
	uid = Column(INT, index=True)
	date = Column(DATE, index=True, default=DateTimeLibrary.date.today)
	nid = Column(INT)
	cid = Column(INT, index=True)
	pvpid = Column(INT)
	pveid = Column(INT)
	coopid = Column(INT)
	openworldid = Column(INT)
	otherid = Column(INT)

	userModel = relationship("User", primaryjoin="remote(User.uid) == foreign(UserHistory.uid)")
	nicknameModel = relationship("Nickname", primaryjoin="remote(Nickname.nid) == foreign(UserHistory.nid)")
	pvpModel = relationship("PVP", primaryjoin="remote(PVP.pvpid) == foreign(UserHistory.pvpid)")
	pveModel = relationship("PVE", primaryjoin="remote(PVE.pveid) == foreign(UserHistory.pveid)")
	coopModel = relationship("COOP", primaryjoin="remote(COOP.coopid) == foreign(UserHistory.coopid)")
	openworldModel = relationship("OpenWorld", primaryjoin="remote(OpenWorld.openworldid) == foreign(UserHistory.openworldid)")
	otherModel = relationship("Other", primaryjoin="remote(Other.otherid) == foreign(UserHistory.otherid)")

	def __repr__(self):
		return "<UserHistory {0}>".format(self.uhid)
	#end define
#end class

class Nickname(Base):
	__tablename__ = "nicknames"

	nid = Column(INT, primary_key=True)
	nickname = Column(String(32, collation="utf8_bin"), nullable=False) # max user nickname length = 16

	def __repr__(self):
		return "<Nickname {0}>".format(self.nickname)
	#end define
#end class

class PVP(Base):
	__tablename__ = "pvps"

	pvpid = Column(INT, primary_key=True)
	gamePlayed = Column(INT)
	gameWin = Column(INT)
	totalAssists = Column(INT)
	totalBattleTime = Column(BIGINT)
	totalDeath = Column(INT)
	totalDmgDone = Column(BIGINT)
	totalHealingDone = Column(BIGINT)
	totalKill = Column(INT)
	totalVpDmgDone = Column(BIGINT)

	def __repr__(self):
		return "<PVP {}>".format(self.gamePlayed)
	#end define
#end class

class PVE(Base):
	__tablename__ = "pves"

	pveid = Column(INT, primary_key=True)
	gamePlayed = Column(INT)

	def __repr__(self):
		return "<PVE {}>".format(self.gamePlayed)
	#end define
#end class

class COOP(Base):
	__tablename__ = "coops"

	coopid = Column(INT, primary_key=True)
	gamePlayed = Column(INT)
	gameWin = Column(INT)
	totalBattleTime = Column(BIGINT)


	def __repr__(self):
		return "<COOP {}>".format(self.gamePlayed)
	#end define
#end class

class OpenWorld(Base):
	__tablename__ = "openworlds"

	openworldid = Column(INT, primary_key=True)
	karma = Column(INT)

	def __repr__(self):
		return "<OpenWorld {}>".format(self.karma)
	#end define
#end class

class Other(Base):
	__tablename__ = "others"

	otherid = Column(INT, primary_key=True)
	effRating = Column(INT)
	prestigeBonus = Column(FLOAT)
	accountRank = Column(SMALLINT)

	def __repr__(self):
		return "<Other {}>".format(self.effRating)
	#end define
#end class

class Clan(Base):
	__tablename__ = "clans"

	cid = Column(INT, primary_key=True)

	clanHistoryModel = relationship("ClanHistory", primaryjoin="remote(ClanHistory.cid) == foreign(Clan.cid)", uselist=True)

	def GetClanNameModel(self):
		if self.clanHistoryModel:
			return self.clanHistoryModel[-1].clanNameModel
		else:
			return None
	#end define

	def GetClanRatingModel(self):
		if self.clanHistoryModel:
			return self.clanHistoryModel[-1].clanRatingModel
		else:
			return None
	#end define

	def __repr__(self):
		return "<Clan {}>".format(self.cid)
	#end define
#end class

class ClanHistory(Base):
	__tablename__ = "clanshistory"

	chid = Column(INT, primary_key=True)
	date = Column(DATE, index=True, default=DateTimeLibrary.date.today)
	cid = Column(INT, index=True)
	cnid = Column(INT)
	crid = Column(INT)

	clanModel = relationship("Clan", primaryjoin="remote(Clan.cid) == foreign(ClanHistory.cid)")
	clanNameModel = relationship("ClanName", primaryjoin="remote(ClanName.cnid) == foreign(ClanHistory.cnid)")
	clanRatingModel = relationship("ClanRating", primaryjoin="remote(ClanRating.crid) == foreign(ClanHistory.crid)")

	def __repr__(self):
		return "<ClanHistory {}>".format(self.chid)
	#end define
#end class

class ClanName(Base):
	__tablename__ = "clannames"

	cnid = Column(INT, primary_key=True)
	name = Column(String(19, collation="utf8_bin"), nullable=False) # max corp name length = 19
	tag = Column(String(5, collation="utf8_bin")) # max corp tag length = 5

	def __repr__(self):
		return "<ClanName {}>".format(self.name)
	#end define
#end class

class ClanRating(Base):
	__tablename__ = "clanratings"

	crid = Column(INT, primary_key=True)
	pvpRating = Column(INT)
	pveRating = Column(INT)

	def __repr__(self):
		return "<ClanRating crid:{}, pvpRating:{}, pveRating:{}>".format(self.crid, self.pvpRating, self.pveRating)
	#end define
#end class


def model2dict(obj):
	if obj == None:
		return None
	d = dict()
	for column in obj.__table__.columns:
		s = column.name[-2:]
		if "id" == s:
			continue
		d[column.name] = str(getattr(obj, column.name))
	return d
#end define
