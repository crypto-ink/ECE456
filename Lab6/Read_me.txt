There are two filles contained within this zip tcprcmdd.py and tcprcmd.py
neither of this files contain any dependencies on other programs and can be in any directory

tcprcmdd.py must be ran in order to start the server before tcprmcd.py can be ran
in order to comp

in order to compile and run tcprcmdd.py follow this format

python3 tcprcmdd.py [port #]

where [port #] is the port that you would like the server to listen to.

in order to compile and run tcprcmd.py follow this format

python3 tcprcmd.py [host] [port #] [execution_count] [delay_time] '[command]'

where [host] is the machine name of the server we want to contact.
where [port #] is the port that you would like the client to connect to
where [execution_count] is the ammount of time to execute the command
where [delay_time] is the delay between executing commands
where '[command]' is a linux command including its options encompased by ''

an example of both files being ran would be 

node-0: python3 tcprcmdd.py 23456
node-1: python3 tcprcmd.py node-0.pablocorlab06.ch-geni-net.instageni.illinois.edu 23456 3 4 'ls -l'

where node-0 and node-1 are two different machines.