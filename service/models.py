#!/usr/bin/env python3
# -*- coding: utf_8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, String, BIGINT, INT, SMALLINT, FLOAT, DATE, DateTime
from sqlalchemy.orm import relationship
import datetime as DateTimeLibrary


# SQLAlchemy init
Base = declarative_base()

class DataBaseUpdateTime(Base):
	__tablename__ = "times"
	id = Column(BIGINT, primary_key=True)
	name = Column(String(64, collation="utf8_bin"), unique=True)
	datetime = Column(DateTime)

	def __repr__(self):
		return "<Time {}>".format(self.startUpdateDataBaseTime)
	#end define
#end class

class LostUid(Base):
	__tablename__ = "lostuids"
	id = Column(BIGINT, primary_key=True)
	uid = Column(BIGINT, index=True, unique=True)

	def __repr__(self):
		return "<LostUid {}>".format(self.uid)
	#end define
#end class

class User(Base):
	__tablename__ = "users"
	userhistoryModel = relationship("UserHistory", back_populates="userModel")

	uid = Column(INT, primary_key=True)

	def __repr__(self):
		return "<User {0}>".format(self.uid)
	#end define

	def GetNickname(self):
		return self.userhistoryModel[-1].nicknameModel.nickname
	#end define

	def GetNicknameModel(self):
		return self.userhistoryModel[-1].nicknameModel
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
	userModel = relationship("User", back_populates="userhistoryModel")
	nicknameModel = relationship("Nickname", back_populates="userhistoryModel")
	pvpModel = relationship("PVP", back_populates="userhistoryModel")
	pveModel = relationship("PVE", back_populates="userhistoryModel")
	coopModel = relationship("COOP", back_populates="userhistoryModel")
	openworldModel = relationship("OpenWorld", back_populates="userhistoryModel")
	otherModel = relationship("Other", back_populates="userhistoryModel")
	
	uhid = Column(INT, primary_key=True)
	uid = Column(INT, ForeignKey("users.uid"))
	date = Column(DATE, index=True, default=DateTimeLibrary.date.today)
	nid = Column(INT, ForeignKey("nicknames.nid"))
	cid = Column(INT, index=True)
	pvpid = Column(INT, ForeignKey("pvps.pvpid"))
	pveid = Column(INT, ForeignKey("pves.pveid"))
	coopid = Column(INT, ForeignKey("coops.coopid"))
	openworldid = Column(INT, ForeignKey("openworlds.openworldid"))
	otherid = Column(INT, ForeignKey("others.otherid"))

	def __repr__(self):
		return "<UserHistory {0}>".format(self.uhid)
	#end define
#end class

class Nickname(Base):
	__tablename__ = "nicknames"
	userhistoryModel = relationship("UserHistory", back_populates="nicknameModel")

	nid = Column(INT, primary_key=True)
	nickname = Column(String(32, collation="utf8_bin"), nullable=False) # max user nickname length = 16

	def __repr__(self):
		return "<Nickname {0}>".format(self.nickname)
	#end define
#end class

class PVP(Base):
	__tablename__ = "pvps"
	userhistoryModel = relationship("UserHistory", back_populates="pvpModel")

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
	userhistoryModel = relationship("UserHistory", back_populates="pveModel")

	pveid = Column(INT, primary_key=True)
	gamePlayed = Column(INT)

	def __repr__(self):
		return "<PVE {}>".format(self.gamePlayed)
	#end define
#end class

class COOP(Base):
	__tablename__ = "coops"
	userhistoryModel = relationship("UserHistory", back_populates="coopModel")

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
	userhistoryModel = relationship("UserHistory", back_populates="openworldModel")

	openworldid = Column(INT, primary_key=True)
	karma = Column(INT)

	def __repr__(self):
		return "<OpenWorld {}>".format(self.karma)
	#end define
#end class

class Other(Base):
	__tablename__ = "others"
	userhistoryModel = relationship("UserHistory", back_populates="otherModel")

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
	clanHistoryModel = relationship("ClanHistory", back_populates="clanModel")

	cid = Column(INT, primary_key=True)

	def GetClanNameModel(self):
		if self.clanHistoryModel:
			return self.clanHistoryModel[-1].clannameModel
		else:
			return None
	#end define

	def GetClanRatingModel(self):
		if self.clanHistoryModel:
			return self.clanHistoryModel[-1].clanratingModel
		else:
			return None
	#end define

	def __repr__(self):
		return "<Clan {}>".format(self.cid)
	#end define
#end class

class ClanHistory(Base):
	__tablename__ = "clanshistory"
	clanModel = relationship("Clan", back_populates="clanHistoryModel")
	clanNameModel = relationship("ClanName", back_populates="clanHistoryModel")
	clanRatingModel = relationship("ClanRating", back_populates="clanHistoryModel")

	chid = Column(INT, primary_key=True)
	date = Column(DATE, index=True, default=DateTimeLibrary.date.today)
	cid = Column(INT, ForeignKey("clans.cid"))
	cnid = Column(INT, ForeignKey("clannames.cnid"))
	crid = Column(INT, ForeignKey("clanratings.crid"))

	def __repr__(self):
		return "<ClanHistory {}>".format(self.chid)
	#end define
#end class

class ClanName(Base):
	__tablename__ = "clannames"
	clanHistoryModel = relationship("ClanHistory", back_populates="clanNameModel")

	cnid = Column(INT, primary_key=True)
	name = Column(String(19, collation="utf8_bin"), nullable=False) # max corp name length = 19
	tag = Column(String(5, collation="utf8_bin")) # max corp tag length = 5

	def __repr__(self):
		return "<ClanName {}>".format(self.name)
	#end define
#end class

class ClanRating(Base):
	__tablename__ = "clanratings"
	clanHistoryModel = relationship("ClanHistory", back_populates="clanRatingModel")

	crid = Column(INT, primary_key=True)
	pvpRating = Column(INT)
	pveRating = Column(INT)

	def __repr__(self):
		return "<ClanRating crid:{}, pvpRating:{}, pveRating:{}>".format(self.crid, self.pvpRating, self.pveRating)
	#end define
#end class