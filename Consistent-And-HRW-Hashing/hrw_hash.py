import hashlib
import requests
import csv
import json
import sys

HASH_LEN = 6

def calHash(val):
    digest = hashlib.md5(val.encode('utf-8')).hexdigest()[0:HASH_LEN]
    return int(digest, 16)

class HRW(object):
    def __init__(self, servers):
        self.servers = []
        for s in servers:
            self.servers.append(s)

    def calWeight(self, key):
        pos = 0
        maxh = 0
        index = 0
        for srv in self.servers:
            temp = srv + key
            h = calHash(temp)
            if(h > maxh):
                maxh = h
                pos = index
            index += 1
        return pos

    def pushRecord(self, rec, hash):
        pos = self.calWeight(hash)
        node = self.servers[pos]
        url = node + "/api/v1/entries"
        header = {'Content-Type': 'application/json'}
        r = requests.post(url, data=rec, headers=header)
        if(r.status_code == 201):
            return False
        else:
            return True


if __name__ == '__main__':
    servers = ['http://localhost:5000','http://localhost:5001','http://localhost:5002','http://localhost:5003']
    c = HRW(servers)
    filename = sys.argv[1]

    if(filename is None):
    	print("no filename provided!")
    	exit(1)
    
    count = 0
    with open(filename, mode='r') as csv_file:
        start = False
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if(start is False):
                start = True
                continue
            key = line[0]+ ":" + line[2]+ ":" + line[3]
            h = calHash(key)
            val = ",".join(line)
            d = "{ \"" + str(h) + "\":\"" + val + "\" }"
            count += 1
            c.pushRecord(d, str(h))

    print("Uploaded all " + str(count) + " entries.")
    print("Verifying the data.")
    for srv in servers:
        url = srv + "/api/v1/entries"
        r = requests.get(url)
        d = r.json()
        print("GET " + srv)
        print(d)    









