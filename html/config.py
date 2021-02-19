#!/usr/bin/env python3
# -*- coding: utf_8 -*-l

import json


class Config:
	def __init__(self, path):
		self.id = None
		self.url = None
		self.user = None
		self.passwd = None
		self.db = None
		self.host = None
		self.currencies = None
		self.GetConfig(path)
	#end define
	
	def GetConfig(self, path):
		with open(path, 'rt') as file:
			text = file.read()
		#end with
		
		data = json.loads(text)
		self.id = data.get("id")
		self.url = data.get("url")
		self.user = data.get("user")
		self.passwd = data.get("passwd")
		self.db = data.get("db")
		self.host = data.get("host")
		self.currencies = data.get("currencies")
	#end define
#end class