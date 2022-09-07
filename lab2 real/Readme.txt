Readme.txt

There are two files that are contained within this zip Sender.py and Receiver.py

The syntax in order to compile the two files afformentioned are

python3 Sender.py [file_name] [source_ip] [destination ip] [source port] [destination port] [datagram_name] 
python3 Receiver.py [source_ip] [destination ip] [datagram_name]  

In order for the Receiver.py to find the correct checksum the same source_ip and destination_ip must be passed when compiling
This is important that they are the same otherwise the correct checksum will not be calculated
The Receiver.py will also write the contents from file_name into a file with the name "output"