import socket
import sys
import os
import time


host1 = "ts2.scorpclub.ru"
host2 = "localhost"
port = 4800

sock1 = socket.socket()
sock2 = socket.socket()

sock1.connect((host1, port))
sock2.connect((host2, port))

def AddLog(inputText, mode="info"):
	localDate = time.strftime('%d.%m.%Y, %H:%M:%S'.ljust(21, " "))
	modeText = (' [' + mode + '] ').ljust(10, " ")
	text = localDate + modeText + inputText
	logName = (sys.argv[0])[:(sys.argv[0]).rfind('.')]
	file = open(logName + ".log", 'a')
	file.write(text + "\r\n")
	file.close()
	print(text)
#end define

def TcpSend(text, sock):
	sock.send(text.encode())
	data = sock.recv(1024).decode()
	output = data[:data.find("<EOF>")]
	return output
#end define

def General():
	text = "<NumberOfUsersInMySQL>" + "iRuuYn" + "</NumberOfUsersInMySQL>"
	buffer = TcpSend(text, sock1)

	userNumber = int(float(buffer))
	AddLog("Find " + str(userNumber) + " nikname's")

	a = 0
	nickname = "null"

	while (a < userNumber):
		text = "<user>" + str(a) + "</user>"
		buffer = TcpSend(text, sock1)
		if ((a % 15) == 0):
			AddLog(str(a) + "/" + str(userNumber) + " [db1] --> [localhost] nick: " + buffer)
		text = "<nickname>" + buffer + "</nickname>"
		buffer = TcpSend(text, sock2)
		a = a + 1
#end while


myName = (sys.argv[0])[:(sys.argv[0]).rfind('.')]
logName = myName + ".log"

if os.path.isfile(logName):
	os.remove(logName)
#end if
#end if


try:
	General()
except BaseException as err:
	AddLog("Critical error: " + str(err), 'error')
#end try


