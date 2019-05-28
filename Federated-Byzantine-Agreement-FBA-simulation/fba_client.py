
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json
import common
import sys

port = 3000

MESSAGES = [
	"foo:10",
	"bar:30",
	"foo:20",
	"bar:20",
	"foo:30",
	"bar:100"
]

MSGINDEX = 0
ID = 0

def getJson(index):
	global ID
	key, val = MESSAGES[index].split(":")
	msg = common.Message(ID, key, val, common.FBAStates.NEW.value).__dict__
	msg["src"] = "client"
	msg = json.dumps(msg).encode()
	ID += 1
	return msg

class HandleDatagram(DatagramProtocol):
	def sendData(self, data, addr):
		self.transport.write(data, addr);

	def datagramReceived(self, datagram, addr):
		global MSGINDEX, port
		msg = json.loads(datagram)
		if msg['result'] == "OK":
			print("Transaction confirmed by node [{}]".format(repr(addr)))
			if MSGINDEX < len(MESSAGES):
				msg = getJson(MSGINDEX)
				print("Sending next message [{}]".format(repr(msg)))
				self.sendData(msg, ('127.0.0.1', port))
				MSGINDEX += 1


def main():
	global MESSAGES, MSGINDEX, port
	if (len(sys.argv) > 1):
		port = int(sys.argv[1])
	proto = HandleDatagram()
	reactor.listenUDP(0, proto)

	# Send first message
	if(len(MESSAGES) > 0):
		msg = getJson(MSGINDEX)
		print("Sending First message [{}]".format(repr(msg)))
		proto.sendData(msg, ('127.0.0.1', port))
		MSGINDEX += 1

	reactor.run()

if __name__ == '__main__':
	main()