import grpc
import yaml
import sys
import threading
import spartan_messanger_pb2
import spartan_messanger_pb2_grpc
from Crypto.Cipher import AES
from Crypto import Random
import base64

# Some global variables (with some default values, in case we didn't receive any new values for 'em)
config_file = "config.yaml"
address = 'localhost'
port = 3000
users = ""
myname = ""
mygroup = ""
other_user = ""
isBroadcast = False

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class Client:
    def __init__(self):
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = spartan_messanger_pb2_grpc.SpartanMessangerStub(channel)
        self.mygroup = ""
        self.isBroadcast = False
        self.key = "SpartanMessenger"
        if not self.login():
            print("Failed to connect to other user! Exiting.")
            exit(1)
        t = threading.Thread(target=self.listen_incoming_msg, daemon=True)
        t.start()

    def login(self):
        users.remove(myname)
        print("[Spartan] Connected to Spartan Server at port 3000.")
        print("[Spartan] User list: " + str(users))
        if myname in group1:
            self.mygroup = "group1"
            print("You are member of group1: " + str(group1))
        else:
            self.mygroup="group2"
            print("You are member of group2: " + str(group2))
        print("What do you want to do?")
        choice = input("[1] One to one chatting OR\n[2] Group chatting\nYour selection:: ")
        if(choice == "1"):
            self.isBroadcast = False
            while True:
                self.other_user = input("[Spartan] Enter username whom you want to chat with: ")
                if(is_valid_user(self.other_user)):
                    break
                print("Unrecognized username %s! Try again\n" % self.other_user)
        else:
            self.isBroadcast = True
            self.other_user = self.mygroup
        resp = self.conn.Connect(spartan_messanger_pb2.Users(msgFrom=myname, msgTo=self.other_user, isBroadcast=self.isBroadcast))
        return resp.code

    def listen_incoming_msg(self):
        try:
            if self.isBroadcast == True:
                messages = self.conn.ReceiveMsg(spartan_messanger_pb2.Message(fromUser="", toUser=self.mygroup, msg="", isBroadcast=True))
            else:
                messages = self.conn.ReceiveMsg(spartan_messanger_pb2.Message(fromUser=self.other_user, toUser=myname, msg=""))
            if messages:
                for recv_msg in messages:
                    if(recv_msg.fromUser == myname):
                        continue
                    m = self.decrypt(recv_msg.msg)
                    print("[" + recv_msg.fromUser + "] " + str(m, 'utf-8') + "\n")
        except Exception:
            print("Exception: Thread interrupted! Exception: " + Exception)

    def send_message(self):
        message = input("\n[" + myname + "] > ")
        if message is not '':
            msg = spartan_messanger_pb2.Message()
            msg.fromUser = myname
            if self.isBroadcast == True:
                msg.toUser = self.mygroup
                msg.isBroadcast = True
            else:
                msg.toUser = self.other_user
            msg.msg = self.encrypt(message)
            self.conn.SendMsg(msg)

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))


def run():
    c = Client()
    while True:
        #if (not self.other_user):
        c.send_message()

def is_valid_user(uname):
    if (uname in users):
        return 1
    return 0


if __name__ == '__main__':
    # Read the YAML file for config
    try:
        stream = open(config_file, 'r')
        config = yaml.load(stream)
        stream.close()
    except:
        print("ERROR: Unable to read config file!")
        exit(1)

    # Fetch port number and user-list
    port = config['port']
    users = config['users']
    group1 = config['groups']['group1']
    group2 = config['groups']['group2']

    # Display usage if no username is provided
    if (len(sys.argv) < 2):
        print("Usage: " + sys.argv[0] + " <username>")
        exit(1)

    # Get my username from command-line args
    myname = sys.argv[1]
    if (myname is '' or (is_valid_user(myname) == 0)):
        print("Invalid user \"%s\"!\nTry again!!" % myname)
        exit(1)

    # Start client process
    run()
