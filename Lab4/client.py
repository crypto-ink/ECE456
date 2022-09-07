#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import sys
from lab1 import encryption, decryption

def encrypt_messages(file_name):   
    key = ';lkjhgfd'            
    file = open(file_name, "r")
    input = file.read()
    file.close()
    result = encryption(input, key)
    return result

def decrpyt_messages(message):
    key = ';lkjhgfd'
    result = decryption(message, key)
    return result 

def send_messages():
    return    

def print_messages():  
    return 

if __name__ == '__main__':
    s = socket.socket()                                     #creating a socket object
    port = int(sys.argv[3])                                 #setting port to value user specifies 
    host = sys.argv[2] + '.pablolab05.ch-geni-net.instageni.colorado.edu'   #create the proper host name

    print("Running ecnryption, please wait!")
    message = encrypt_messages(sys.argv[1])                 #encrypt the message that we want to send
    message_encoded = str.encode(message)                   #message encoded into bytes
    print("Encryption completed!")

    s.connect((host, port))                                 #connect to specified host and port
    print("Sending message...")
    s.send(message_encoded)                                 #send our encoded message

    print("Receiving data, please wait!")
    last_five_bytes = s.recv(1024)                          # receive the last 5 messages in bytes

    print("Running decryption, please wait!")
    last_five_encrypted = last_five_bytes.decode()          # decode from bytes into string
    last_five = decrpyt_messages(last_five_encrypted)       # decrypt the message that we received
    print(last_five)                                        # print the last five messages

    s.close()                                               # Close the socket when done