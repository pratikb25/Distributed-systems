import pickledb

class Storage:
    def __init__(self, file):
        self.dbfile = file
        self.db = pickledb.load(self.dbfile, auto_dump=True)

    def add(self, key, val):
        if self.db.get(key) is not None:
            v = int(self.db.get(key))
            v += int(val)
        else:
            v = int(val)
        self.db.set(key, v)

    def commit(self):
        # Dump all data from memory to the file
        self.db.dump()

    def reload(self):
        # Reload data
        pickledb.load(self.dbfile, False)

    def printDB(self):
        with open(self.dbfile, 'r') as fp:
            print(fp.read())


