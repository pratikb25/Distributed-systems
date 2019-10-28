import hashlib
import requests
import csv
import json
import sys

HASH_LEN = 6

def calHash(val):
    digest = hashlib.md5(val.encode('utf-8')).hexdigest()[0:HASH_LEN]
    return int(digest, 16)

class ConsistentHash(object):
    def __init__(self, servers):
        self.nodes = servers
        self.node_hashes = []
        for s in servers:
            digest = calHash(s)
            self.node_hashes.append(digest)
        self.node_hashes.sort()

        # Generated a HashMap of <server_hash, server_url> pairs
        self.node_map = {calHash(node):node for node in self.nodes}

    def lookup(self, hash):
        for i in range(0, len(self.node_hashes)):
            if(int(self.node_hashes[i]) >= hash):
                return self.node_map[self.node_hashes[i]]
        return self.node_map[self.node_hashes[0]]

    def pushRecord(self, rec, hash):
        node = self.lookup(hash)
        url = node + "/api/v1/entries"
        header = {'Content-Type': 'application/json'}
        r = requests.post(url, data=rec, headers=header)
        if(r.status_code == 201):
            return False
        else:
            return True


if __name__ == '__main__':
    servers = ['http://localhost:5000','http://localhost:5001','http://localhost:5002','http://localhost:5003']
    c = ConsistentHash(servers)
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
            c.pushRecord(d, h)

    print("Uploaded all " + str(count) + " entries.")
    print("Verifying the data.")
    for srv in servers:
        url = srv + "/api/v1/entries"
        r = requests.get(url)
        d = r.json()
        print("GET " + srv)
        print(d)    


