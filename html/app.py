#!/usr/bin/env python3
# -*- coding: utf_8 -*-l

'''
Before starting this script run the following steps:
1. Install:
	apt-get install mysql-server mysql-client libmysqlclient-dev apache2 libapache2-mod-wsgi-py3
	pip3 install mysqlclient sqlalchemy flask
2. Create user and DB in MySQL
	CREATE USER '<mysql-user-name>'@'localhost' IDENTIFIED BY '<mysql-password>';
	GRANT ALL PRIVILEGES ON api.* TO '<mysql-user-name>'@'localhost';
	CREATE DATABASE api;
3. Move all files in this directory into '/var/www/flask'
4. Write into '/etc/apache2/sites-enabled/000-default.conf':
<VirtualHost *:80>
        ServerName <server-ip-or-domain-name>
        WSGIDaemonProcess app user=www-data group=www-data threads=5
        WSGIScriptAlias / /var/www/flask/app.wsgi
        <Directory /var/www/flask>
                WSGIProcessGroup app
                WSGIApplicationGroup %{GLOBAL}
                Require all granted
        </Directory>
        LogLevel info
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
5. a2enmod wsgi
6. Restart apache2
'''


import os
import json
import threading
from urllib.request import urlopen
from urllib.parse import urlencode
from flask import Flask, abort, send_from_directory
from models import *
from config import Config
from database import DataBase
from response import Response

app = Flask(__name__)
# cnfpath = os.path.join(app.root_path, "config.json")
# cnf = Config(cnfpath)
# db = DataBase(cnf.user, cnf.passwd, cnf.db, cnf.host)
db = DataBase("editor", "passwd44c4", "schistory", "127.0.0.1")
resp = Response()



###
### Дополнительные функции
###
def Init():
	app.secret_key = os.urandom(42)
	app.config["JSON_SORT_KEYS"] = False
	app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
#end define


###
### Статические страницы
###
@app.route("/api/v2/userinfo/<int:uid>")
@app.route("/api/v2/userinfo/<int:uid>/<int:limit>")
def ApiUserinfo(uid, limit=30):
	data = dict()
	data["pnum"] = db.GetUserPassNum(uid)
	data["history"] = db.GetUserHistor(uid, limit)
	inf = resp.Inf(data)
	return inf
#end define

@app.route("/api/v2/lostuids")
@app.route("/api/v2/lostuids/<int:limit>")
def ApiLostuids(limit=30):
	data = dict()
	lostuids = db.GetLostUids(limit)
	data["length"] = len(lostuids)
	data["lostuids"] = lostuids
	return data
#end define

@app.route("/api/v2/claninfo/<int:cid>")
@app.route("/api/v2/claninfo/<int:cid>/<int:limit>")
def ApiClaninfo(cid, limit=30):
	data = dict()
	history = db.GetClanHistory(cid, limit, True)
	data["length"] = len(history)
	data["history"] = history
	return data
#end define

@app.route("/api/v2/status")
def ApiStatus():
	data = dict()
	tableStatus = db.GetTableStatus("usershistory")
	times = db.GetTimes()
	data.update(times)
	rows = round(tableStatus.Rows / 10**6, 2)
	dataLength = round(tableStatus.Data_length / 10**9, 2)
	indexLength = round(tableStatus.Index_length / 10**9, 2)
	data["rows"] = "{rows} M".format(rows=rows)
	data["dataLength"] = "{dataLength} Gb".format(dataLength=dataLength)
	data["indexLength"] = "{indexLength} Gb".format(indexLength=indexLength)
	if times.popitem()[1] > times.popitem()[1]:
		data["isUpdateCompleted"] = True
	else:
		data["isUpdateCompleted"] = False
	return data
#end define





###
### Статические файлы
###
@app.route("/favicon.ico")
def favicon():
	name = "favicon.ico"
	path = os.path.join(app.root_path, "static")
	mimetype = "image/vnd.microsoft.icon"
	return send_from_directory(path, name, mimetype=mimetype)
#end define

@app.route("/robots.txt")
def robots():
	name = "robots.txt"
	path = os.path.join(app.root_path, "static")
	return send_from_directory(path, name)
#end define

@app.route("/license.html")
def license():
	name = "license.html"
	path = os.path.join(app.root_path, "static")
	return send_from_directory(path, name)
#end define

@app.route("/error.html")
def error():
	name = "error.html"
	path = os.path.join(app.root_path, "static")
	return send_from_directory(path, name)
#end define



###
### Кастомные страницы ошибок
###
@app.errorhandler(400)
def Err400(error):
	err = resp.Err("Bad Request", 400)
	return err
#end define

@app.errorhandler(401)
def Err401(error):
	err = resp.Err("Unauthorized", 401)
	return err
#end define

@app.errorhandler(403)
def Err403(error):
	err = resp.Err("Forbidden", 403)
	return err
#end define

@app.errorhandler(404)
def Err404(error):
	err = resp.Err("Not Found", 404)
	return err
#end define

@app.errorhandler(500)
def Err500(error):
	err = resp.Err("Internal Server Error", 500)
	return err
#end define

@app.errorhandler(502)
def Err502(error):
	err = resp.Err("Bad Gateway", 502)
	return err
#end define



###
### Старт программы
###
if __name__ == "__main__":
	Init()
	app.run(host="0.0.0.0", port=8080)
#end if


