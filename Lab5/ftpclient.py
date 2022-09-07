import os
import socket               # Import socket module
import sys
from lab1 import encryption, decryption

def encrypt_messages(file_name):   
    # key = ';lkjhgfd'            
    # file = open(file_name, "r")
    # input = file.read()
    # file.close()
    # result = encryption(input, key)
    result = "FUNCTION encrypt_messages() STILL NEEDS TO BE IMPLEMTED"
    print(result)
    return result

def decrpyt_messages(message):
    key = ';lkjhgfd'
    result = decryption(message, key)
    return result 

def file_size(file_name):                   # takes a file name and returns the fize 
    file_size = os.path.getsize(file_name)  # of the file in bytes as an int
    return file_size

def int_to_bytes(integer):
    num_bytes = integer.to_bytes(16, byteorder='big')
    return num_bytes


def send_packet(sending_socket, file_to_send):   #takes the socket which should be sending packets which packet frame to send
    sending_socket.send(file_to_send.read(1024))
    sending_socket.recv(1024)
    return   

if __name__ == '__main__':
    # sys.aargv[1] is the file we want to send
    # sys.argv[2] is the ip/hostname we want to connect to. 
    # sys.argv[3] contains the port that we want to connect to

    if len(sys.argv) != 4:  # check if the correct ammount of arguements are used if not quit
        print("Please enter data file name, destination IP(or domain name), destination port number correctly!")
        exit()

    s = socket.socket()                                     #creating a socket object
    port = int(sys.argv[3])                                 #setting port to value user specifies 
    host = sys.argv[2] + '.pablolab06.ch-geni-net.instageni.colorado.edu'   #create the proper host name

    print("Running ecnryption, please wait!")
    print("Encryption completed!")

    file_size = file_size(sys.argv[1])

    s.connect((host, port))                                 #connect to specified host and port
    print("Waiting for server's permission...")
    s.send(str.encode(sys.argv[1]))                         #send file name
    s.send(int_to_bytes(file_size))                         #send file size 
    accepted = s.recv(1024)                                 #check to see if the file was accepted
    
    packets = file_size/1024
    if(file_size % 1024 != 0):                              #check if any of packet would still not be sent
        packets += 1
    if accepted.decode() == 'y':                                     #check to see if accepted == y 
        print(f"Sending file, size: {file_size}")
        file = open(sys.argv[1], "rb")
        count = 0
        while count < packets:                             #while there are still packets to send to server send packets
          send_packet(s, file)                             # sending packets using s at frame count
          count += 1
        s.recv(1024)
        file.close
        print("File sent to server.")
    else: 
        print("Server did not accept file transfer")


    s.close()                                               # Close the socket when done
   