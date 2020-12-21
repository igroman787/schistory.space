#!/usr/bin/env python3
# -*- coding: utf_8 -*-l

import time
from flask import jsonify, make_response






class Response:
	def Inf(self, data, msg="ok"):
		response = self.Resp(data=data, msg=msg)
		return response
	#end define

	def Err(self, msg, code):
		response = self.Resp(err=True, msg=msg, code=code)
		return response
	#end define

	def Resp(self, **kwargs):
		rdata = dict()
		rdata["error"] = kwargs.get("err", False)
		rdata["status"] = kwargs.get("code", 200)
		rdata["message"] = kwargs.get("msg", "Ok")
		data = kwargs.get("data")
		if data:
			rdata["timestamp"] = self.TS()
			rdata["data"] = data
		jdata = jsonify(rdata)
		response = make_response(jdata)
		return response
	#end define

	def TS(self):
		t = time.time()
		ts = int(t)
		return ts
	#end define
#end class
