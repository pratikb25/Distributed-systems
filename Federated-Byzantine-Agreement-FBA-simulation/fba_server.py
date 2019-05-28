
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import sys, json, uuid, time
from Storage import Storage
import common

port = 3000
sleep_interval_sec = 1

# Sleep for 3 sec
def sleepN():
	global sleep_interval_sec
	time.sleep(sleep_interval_sec)

class Server(DatagramProtocol):
	# Constructor
	def __init__(self):
		global port
		self.port = port 			# Remember our port number
		self.filename = "assignment_" + str(port) + ".db" 	# DB file name
		self.db = Storage(self.filename)						# Initialize the DB
		self.isPrimaryNode = False	# Flag to identify if we are primary node that will talk to the client
		self.quorum = common.constructQuorum(int(port))	# Create my quorum
		self.logger("My Quorum is {}".format(str(self.quorum)))	# Print the quorum
		self.broadcastFlags = dict()	# Flags to keep track of broadcast so that we don't end up in indefinite loop
		self.ballots = dict()		# Temporary buffers to store the intermediate states of a
		self.senderlist = list() 	# List of ports of the nodes who send replies
		self.clientport = None		# The client port. Set when this is the primary node
		self.readyToCommit = False	# Flag to identify if we are ready commit

	def logger(self, log_message):
		role = ""
		if self.isPrimaryNode is not None and self.isPrimaryNode == True:
			role = "Primary "
		print("[{}Node {}]: {}".format(role, self.port, log_message))

	def displayDatabase(self):
		self.logger("Here are the contents of my PickleDB:\n")
		self.db.printDB()

	# IMPORTANT: Always call at the very end
	def resetMe(self):
		self.broadcastFlags = dict()
		self.ballots.clear()
		self.senderlist.clear()
		self.readyToCommit = False
		self.isPrimaryNode = False
		self.clientport = None

	# Check if it is majority
	def isMajority(self):
		for port in self.quorum:
			if port not in self.senderlist:
				return False
		return True

	def handleState(self, id, key, val, type, senderport):
		self.senderlist.append(senderport)
		msgStr = common.getMessageStr(type)
		print("Received {} from node[{}]: id[{}], msg[{}], val[{}]".format(msgStr, senderport, id, key, val))
		self.conditionalBroadcast(type, id, key, val)
		sleepN() # Sleep for a few seconds to ensure that all the member nodes have processed their messages
		if self.isMajority():
			print("Received majority for state {}".format(msgStr))
			self.senderlist.clear()
			if(type != common.FBAStates.CONFIRM.value):
				type = common.getNextState(type)
				print("Going to next state")
				self.conditionalBroadcast(type, id, key, val)
			else:
				print("Committed to DB!!!")
				self.readyToCommit = True
				self.db.add(key, val)
				self.displayDatabase()

	# Listener callback function
	def datagramReceived(self, datagram, address):
		msg = json.loads(datagram)
		id = msg["id"]
		key = msg["key"]
		val = msg["val"]
		type = int(msg["type"])
		senderport = address[1]

		if("src" in msg):
			self.isPrimaryNode = True
			self.clientport = senderport
		else:
			self.isPrimaryNode = False

		if(type == common.FBAStates.NEW.value):
			if(self.isPrimaryNode):
				self.logger("I am Primary, Bitch.")
			self.logger("********************* Processing new msg ID [{}] **********************".format(id))
			print("New transaction received from client: id[{}], msg[{}], val[{}], type[{}]".format(id, key, val, type))
			self.conditionalBroadcast(type, id, key, val)

			# Sleep for a few seconds
			sleepN()

			# Change to INIT state and broadcast
			type = common.FBAStates.INIT.value
			self.conditionalBroadcast(type, id, key, val)
		else:
			self.handleState(id, key, val, type, senderport)

		if(self.readyToCommit == True):
			if(self.clientport is not None):
				result = {"result": "OK"}
				result = json.dumps(result).encode()
				self.sendData(result, ('127.0.0.1', self.clientport))
			self.resetMe() # Committed the transaction and repied to the client. Noe, reset all and be ready for next transaction

	def conditionalBroadcast(self, type, id, key, val):
		if type in self.broadcastFlags:
			if self.broadcastFlags[type] == False:
				t = common.Message(id, key, val, type).__dict__
				t = json.dumps(t).encode()
				self.broadCast(t)
				self.broadcastFlags[type] = True
		else:
			t = common.Message(id, key, val, type).__dict__
			t = json.dumps(t).encode()
			self.broadCast(t)
			self.broadcastFlags[type] = True

	# Param: data = encoded Json
	def broadCast(self, data):
		for port in self.quorum:
			self.sendData(data, ('127.0.0.1', port))

	# Param: 	data = encoded Json
	#			address = tuple(<IP>, <Port>)
	def sendData(self, data, address):
		self.transport.write(data, address)

	def startPortListener(self):
		global port
		# Initialize the port and UDP listener
		self.port = int(port)
		reactor.listenUDP(self.port, self)
		reactor.run()

if __name__ == '__main__':
	if(len(sys.argv) > 1):
		port = sys.argv[1]
	srv = Server()
	srv.startPortListener()