# This is server process that handles chatting between clients
# Import package to support multiprocessing
from concurrent import futures

# Import auto-generated python gRPC code
import grpc
import spartan_messanger_pb2
import spartan_messanger_pb2_grpc

# Import other auxiliary packages
import time
import yaml

# Some global variables (with some default values, in case we didn't receive any new values for 'em)
config_file = "config.yaml"
address = '[::]'
port = 3000
users = ""
group1 = ""
group2 = ""
chats = {}
group_chats = {}
max_num_messages_per_user = 5 # Default LRU cache limit

def generateKey(string1, string2):
    key = string1.lower() + string2.lower()
    key = ''.join(sorted(key))
    return key


def isMember(sendername, groupname):
    if groupname == "group1":
        if sendername in group1:
            return True
    else:
        if sendername in group2:
            return True
    return False

#### Messsage storage format
class Message:
    def __init__(self, sender, message):
        self.sender = sender
        self.message = message

    def getSender(self):
        return self.sender.lower()

    def getMessage(self):
        return self.message

    def setSender(self, sender):
        self.sender = sender

    def setMessage(self, message):
        self.message = message
###################################


#### Custom implementation of LRU cache to hold messages
class myLRU:
    def __init__(self, maxsize = 5):
        self.table = []
        if maxsize < 0:
            maxsize = 5                     # Some default length for the list
        self.maxsize = maxsize              # Maximum size of table allowed
        self.last_read_index = -1                # No items

    def insert(self, item):
        if len(self.table) == self.maxsize:
            self.table.pop(0)
            self.table.append(item)
            if self.last_read_index >= 0:
                self.last_read_index -= 1;
            else:
                self.last_read_index = -1
        else:
            self.table.append(item)

    def get(self, index):
        if(index < 0):
            return None
        if not self.table[index]:
            return None
        return self.table[index]

    def getLastIndex(self):
        return self.last_read_index

    def resetLastIndex(self):
        self.last_read_index = -1;

    def setLastIndex(self, value):
        self.last_read_index = value

    def size(self):
        return len(self.table)
############### End of LRU Cache


class SpartanServer(spartan_messanger_pb2_grpc.SpartanMessangerServicer):
    def __init__(self):
        self.isBroadcast = False     # Dictionary to store messages
        self.mygroup = None
        stream = open(config_file, 'r')
        config = yaml.load(stream)
        stream.close()
        self.group1 = config['groups']['group1']
        self.group2 = config['groups']['group2']

    def Connect(self, request, context): # Request msg: {Myname(msgFrom), mygroup(msgTo), isBroadcast=true}
        global group1, group2
        key = request.msgTo
        isBroadcast = request.isBroadcast
        if(isBroadcast == True):
            if key not in group_chats:
                print("[Group] Creating new buffer for key " + key)
                group_chats[key] = myLRU(max_num_messages_per_user)
                group_chats[key].resetLastIndex()
        else:
            if key not in chats:
                print("Creating new buffer for key " + key)
                chats[key] = myLRU(max_num_messages_per_user)
                chats[key].resetLastIndex()
        return spartan_messanger_pb2.Status(code=1)

    def ReceiveMsg(self, request, context):     # Request msg: {myname(fromUser)="", mygroup(toUser)=groupname, msg="", isBroadcast=true}
        key = request.toUser
        isBroadcast = request.isBroadcast
        if(isBroadcast == True):
            mailbox = group_chats
        else:
            mailbox = chats

        if key not in mailbox:
                mailbox[key] = myLRU(max_num_messages_per_user)

        all_chats = mailbox[key]
        all_chats.resetLastIndex()
        while True:
            lastIndex = all_chats.getLastIndex() + 1
            while(lastIndex < all_chats.size()):
                next_msg = all_chats.get(lastIndex)
                lastIndex += 1
                if isBroadcast == True:
                    if isMember(next_msg.getSender(), request.toUser):
                        yield spartan_messanger_pb2.Message(fromUser=next_msg.getSender(), toUser=request.toUser, msg=next_msg.getMessage())
                else:
                    if next_msg.getSender() == request.fromUser:
                        yield spartan_messanger_pb2.Message(fromUser=request.fromUser, toUser=request.toUser, msg=next_msg.getMessage())
                if(lastIndex == all_chats.size()):
                    all_chats.setLastIndex(all_chats.size() - 1)

    def SendMsg(self, request, context):    # Request: {myname, mygroup, msg, isBroadcast}
        print(request.fromUser + " to " + request.toUser + ": " + request.msg)
        key = request.toUser.lower()
        isBroadcast = request.isBroadcast
        if isBroadcast == True:
            mailbox = group_chats
            print("Sending to group " + key)
        else:
            print("Sending to usr " + key)
            mailbox = chats
        if key not in mailbox:
            mailbox[key] = myLRU(max_num_messages_per_user)
        all_chats = mailbox[key]
        all_chats.insert(Message(request.fromUser, request.msg))
        return spartan_messanger_pb2.Empty()


SERVER_SLEEP_TIME = (60 * 60)

def main():
    # Read the YAML file for config
    try:
        stream = open(config_file, 'r')
        config = yaml.load(stream)
        stream.close()
    except:
        print("ERROR: Unable to read config file!")
        exit(1)

    # Fetch port number and user-list
    global port, group1, group2, max_num_messages_per_user
    port = config['port']
    group1 = config['groups']['group1']
    group2 = config['groups']['group2']
    max_num_messages_per_user = config['max_num_messages_per_user'] # LRU cache limit

    # TODO Validate incoming user => users = config['users']

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    spartan_messanger_pb2_grpc.add_SpartanMessangerServicer_to_server(SpartanServer(), server)
    server.add_insecure_port(address + ':' + str(port))
    server.start();
    print("Started server started on port " + str(port) + "\n")
    try:
        while True:
            time.sleep(SERVER_SLEEP_TIME);
    except KeyboardInterrupt:
        print("\n")
        server.stop(0);

if __name__ == '__main__':
    main()
