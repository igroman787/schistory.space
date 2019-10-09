import socket
from updateDatabase import *


host = ""
port = 4800
packetLength = 1024

sock = socket.socket()
sock.bind((host, port))
sock.listen(50)


class Connect(threading.Thread):
	def __init__(self, conn, addr):
		self.conn = conn
		self.addr = addr
		threading.Thread.__init__(self)
	def run (self):
		try:
			Main(self)
		except ConnectionResetError:
			AddLog("The client forcibly severed the connection: " + str(self.addr), "error")
#end define

def Main(self):
	buffer = "null"
	while True:
		outputText = "null"
		data = self.conn.recv(packetLength)
		if len(data) < 1:
			return
		try:
			inputText = data.decode("UTF-8").replace("<EOF>", "")
		except UnicodeDecodeError:
			AddLog("The package is not a text", "error")
			return
		#end try

		try:
			AddLog("Get the package: " + inputText, "debug")
			outputText, buffer = Reaction(inputText, buffer)
		except Exception as err:
			AddLog(str(err), "error")
		#end try
		
		if outputText != "null":
			myBytes = outputText.encode("UTF-8")
			self.conn.send(myBytes + b"<EOF>")
#end define

def Reaction(inputText, buffer):
	AddLog("Start Reaction", "debug")
	outputText = "null"
	if ("<nickname>" in inputText):
		outputText = InputNicknameReaction(inputText)
	return outputText, buffer
#end define

def InputNicknameReaction(inputText):
	AddLog("Start InputNicknameReaction", "debug")
	nickname = Pars(inputText, "<nickname>", "</nickname>")
	
	# Checking the correctness of the nickname
	result = IsNicknameGood(nickname)
	if result < 0:
		AddLog("nickname is not good", "debug")
		return "nickname is not good"
	
	# Get data from SC API
	arr = GetDataFromSC(nickname)
	if arr == None: # If all is bad
		AddLog("I'm crying because I can't get a candy ;(", "error")
		return "I'm crying because I can't get a candy ;("
	elif arr["code"] == 1: # If invalid nickname
		AddLog("user not found", "debug")
		return "user not found"
	elif arr["code"] == 0: # If everything is ok
		uid = arr["data"]["uid"]
		nickname = arr["data"]["nickName"]
		AddNicknameToDB(uid, nickname)
		return "ok"
#end define

def AddNicknameToDB(uid, nickname):
	AddLog("Start AddNicknameToDB", "debug")
	
	# Create MySQL connect
	engine, session = CreateConnectToDB()

	# Get module from DB
	userModel = session.query(User).filter_by(uid=uid).first()
	if not userModel:
		userModel = User(uid=uid)
		nicknameModel = Nickname(nickname=nickname)
		userhistoryModel = UserHistory(userModel=userModel, nicknameModel=nicknameModel)
		session.add(userhistoryModel)
		AddLog("Find new user {0}".format(nickname))
	elif (userModel.GetNickname() != nickname):
		nicknameModel = Nickname(nickname=nickname)
		userhistoryModel = UserHistory(userModel=userModel, nicknameModel=nicknameModel)
		session.add(userhistoryModel)
		AddLog("Find new nickname {0}".format(nickname))
	#end if

	# Get module from DB
	lostuid = session.query(LostUid).filter_by(uid=uid).first()
	if lostuid:
		session.query(LostUid).filter_by(uid=uid).delete()
	#end if

	# Close MySQL connect
	CloseDBConnect(engine, session)
#end define

def IsNicknameGood(nickname):
	goodsign_s = "q w e r t y u i o p a s d f g h j k l z x c v b n m Q W E R T Y U I O P A S D F G H J K L Z X C V B N M 1 2 3 4 5 6 7 8 9 0 @ . _".split(' ')
	user_nikname_0 = list(nickname)
	nickname_cycle = 0
	while nickname_cycle < len(user_nikname_0):
		c_gn_1 = user_nikname_0[nickname_cycle]
		if c_gn_1 not in goodsign_s:
			return -1
		nickname_cycle = nickname_cycle + 1
	return 0
#end define

def Pars(inputText, startScan, endScan):
	text_0 = inputText[inputText.find(startScan) + len(startScan):]
	outputText = text_0[:text_0.find(endScan)]
	return outputText
#end define

def HideIpAddress(addr):
	ip = addr[0]
	ip_arr = ip.split('.')
	output = "*.*." + ip_arr[2] + "." + ip_arr[3]
	return output
#end define


###
### Start of the program
###

Init()

AddLog("Running the SCHistoryService server on the port: " + str(port))
while True:
	try:
		time.sleep(1)
		conn, addr = sock.accept()
		AddLog("--- --- ---")
		AddLog("There is an incoming connection: " + HideIpAddress(addr))
		Connect(conn, addr).start()
	except Exception as err:
		AddLog("Critical error: " + str(err), "error")
# end while
