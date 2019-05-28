# Simulation of Federated Byzantine Agreement (FBA) consensus protocol in Python 3

## Description:
Implemented a key-value datastore service that persists user wallet info: username and balance. If a user does not exist in DB yet, 
the service will create a new entry with a given value. Otherwise, the user wallet will be updated with the new amount.

- The simulation uses PickleDB to store the transaction messages after consensus is formed.
- The server nodes communicate with each other over UDP.
- Since this is just a simulation, each node has quorum size of 3 containing the other servers.
- The implementation works with a cluster of 4 server nodes:
- Run the 4 server nodes as follows: <br />
python3 fba_server.py 3000 <br />
python3 fba_server.py 3001 <br />
python3 fba_server.py 3002 <br />
python3 fba_server.py 3003 <br />

- There is 1 client node that sends the transaction messages to the primary node in the cluster. Run the client as follows: <br />
python3 fba_client.py 3000 <br />

