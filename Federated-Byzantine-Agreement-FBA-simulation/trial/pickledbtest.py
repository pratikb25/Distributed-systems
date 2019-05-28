import pickledb

db = pickledb.load("./sampledb.db", False)
db.set("empid", "1001")
db.set("name", "John Doe")
db.dump()
db.set("empid", "2001")
val = db.get('empid')
print("Key is %s, value is %s" % ('empid', val))
db.dump()
print("Key is %s, value is %s" % ('empid', val))
