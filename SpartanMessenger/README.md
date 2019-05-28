**Use-case:**
=============
- The client program asks the user if he/she wants to initiate one to one chat or a group conversation. 
- If he/she chooses 'one-to-one' conversation, the program asks for other username whom he/she wants to chat with.
- If he/she chooses 'group' conversation, a prompt is displayed where client can type in the message which will be broadcasted to the members of its group only.

**A. One-to-one chatting:**
===========================
Server Command: python3 server.py
Client Command: python3 client.py <username>

**Sample run:**
---------------
**[Server]**
$ python3 server.py
Started server started on port 3000
Creating new buffer for key bob
alice to bob: hi
Sending to usr bob
bob to alice: Hey
Sending to usr alice
alice to bob: How r u?
Sending to usr bob
bob to alice: I am fine. And, how r u doing?
Sending to usr alice
alice to bob: Good. Just busy with the classes
Sending to usr bob
bob to alice: Good. 


**[Client "Alice"]**
[Spartan] Connected to Spartan Server at port 3000.
[Spartan] User list: ['bob', 'charlie', 'eve', 'foo', 'bar', 'baz', 'qux']
You are member of group1: ['alice', 'bob', 'charlie', 'eve']
What do you want to do?
[1] One to one chatting OR
[2] Group chatting
Your selection:: 1
[Spartan] Enter username whom you want to chat with: bob
[alice] > hi
[alice] > 
[bob] Hey
[alice] > How r u?
[alice] > 
[bob] I am fine. And, how r u doing?
[alice] > Good. Just busy with the classes

**[Client Bob]**
[Spartan] Connected to Spartan Server at port 3000.
[Spartan] User list: ['alice', 'charlie', 'eve', 'foo', 'bar', 'baz', 'qux']
You are member of group1: ['alice', 'bob', 'charlie', 'eve']
What do you want to do?
[1] One to one chatting OR
[2] Group chatting
Your selection:: 1
[Spartan] Enter username whom you want to chat with: alice

[bob] > 
[alice] hi
[bob] > Hey
[bob] > 
[alice] How r u?
[bob] > I am fine. And, how r u doing?
[bob] > 
[alice] Good. Just busy with the classes



**B. Group chatting:**
======================
Server Command: python3 server.py
Client Command: python3 client.py <username>

**Sample run:**
---------------
**[Server]**
$ python3 server.py
Started server started on port 3000
[Group] Creating new buffer for key group1
alice to group1: hi
Sending to group group1
bob to group1: hello everyone
Sending to group group1
eve to group1: hey, how r u guys doing?
Sending to group group1

**[Client Alice]**
[Spartan] Connected to Spartan Server at port 3000.
[Spartan] User list: ['bob', 'charlie', 'eve', 'foo', 'bar', 'baz', 'qux']
You are member of group1: ['alice', 'bob', 'charlie', 'eve']
What do you want to do?
[1] One to one chatting OR
[2] Group chatting
Your selection:: 2
[alice] > hi
[alice] > 
[bob] hello everyone
[eve] hey, how r u guys doing?


**[Client "Bob"]**
[Spartan] Connected to Spartan Server at port 3000.
[Spartan] User list: ['alice', 'charlie', 'eve', 'foo', 'bar', 'baz', 'qux']
You are member of group1: ['alice', 'bob', 'charlie', 'eve']
What do you want to do?
[1] One to one chatting OR
[2] Group chatting
Your selection:: 2
[alice] hi
[bob] > hello everyone
[bob] > 
[eve] hey, how r u guys doing?


**[Client "eve"]**
[Spartan] Connected to Spartan Server at port 3000.
[Spartan] User list: ['alice', 'bob', 'charlie', 'foo', 'bar', 'baz', 'qux']
You are member of group1: ['alice', 'bob', 'charlie', 'eve']
What do you want to do?
[1] One to one chatting OR
[2] Group chatting
Your selection:: 2
[alice] hi
[bob] hello everyone
[eve] > 
[eve] > hey, how r u guys doing?
[eve] > 

