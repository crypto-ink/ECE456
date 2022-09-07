There are three files contained within this zip client.py and server.py lab1.py
Client.py and server.py are both dependent on lab1.py thus a copy of lab1.py must be in the same directory as the respective files

server.py must be first ran before client.py can be ran

in order to compile and run server.py follow this format

python3 server.py [port #]

where [port #] is the port that you would like the server to listen to.

in order to compile and run client.py follow this format

python3 client.py [file_name] [host] [port #]

where [file_name] is the name of the file that contains the messsage to be sent
where [host] is the machine name of the server we want to contact.
where [port #] is the port that you would like the client to connect to.

an example of both files being ran would be

node-0: python3 server.py 23456
node-1: python3 client.py node_1_message.txt node-0 23456

where node-0 and node-1 are two different machines.