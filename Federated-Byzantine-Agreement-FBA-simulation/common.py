import enum

class Ballot:
    def __init__(self, id, msg, type):
        self.id = id
        self.message = msg
        self.type = type
        self.replies = list()

class Quorum:
    def __init__(self, lst=[]):
        self.members = lst

    def add(self, node):
        if node not in self.members:
            self.lst.append(node)

    def contains(self, node):
        return node in self.members

def constructQuorum(myPort):
    list = []
    for p in range(3000, 3004):
        if(p == myPort):
            continue
        list.append(p)
    return list

class Message:
    def __init__(self, id, key, val, type):
        self.id = id
        self.key = key
        self.val = val
        self.type = type

class FBAStates(enum.Enum):
    INVALID = -1
    NEW = 0
    INIT = 1
    ACCEPT = 2
    RATIFICATION = 3
    CONFIRM = 4


def getMessageStr(type):
    switcher = {
        FBAStates.INVALID.value: "INVALID",
        FBAStates.NEW.value: "NEW",
        FBAStates.INIT.value: "INIT",
        FBAStates.ACCEPT.value: "ACCEPT",
        FBAStates.RATIFICATION.value: "RATIFICATION",
        FBAStates.CONFIRM.value: "CONFIRM"
    }
    if(type in switcher):
        return switcher[type]
    else:
        return switcher[FBAStates.INVALID.value]

def getNextState(type):
    switcher = {
        FBAStates.INVALID.value: FBAStates.INVALID.value,
        FBAStates.NEW.value: FBAStates.INIT.value,
        FBAStates.INIT.value: FBAStates.ACCEPT.value,
        FBAStates.ACCEPT.value: FBAStates.RATIFICATION.value,
        FBAStates.RATIFICATION.value: FBAStates.CONFIRM.value,
        FBAStates.CONFIRM.value: FBAStates.CONFIRM.value
    }
    if(type in switcher):
        return switcher[type]
    else:
        return FBAStates.INVALID.value

