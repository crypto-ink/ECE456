#!/usr/bin/python           # This is server.py file

from email import message
import socket               # Import socket module
import sys
import datetime
from lab1 import encryption, decryption

def encrypt_message(message):   
    key = ';lkjhgfd'
    result = encryption(message, key)
    return result

def decrpyt_message(message):
    key = ';lkjhgfd'
    result = decryption(message, key)
    return result 

def clean_messages(message_board):
    message_board = [ "------------------------------\n" 
                    + f"Message #{i+1}:\n"
                    + "XXX XXX 00 00:00:00 0000 IP:0.0.0.0\n"
                    + "" for i in range(5)]
    return message_board

def print_messages(message_board):
    for x in message_board:
            print(x)
    return

def add_message(message_board, message):
    for i in range(len(message_board)-1): #loop to move messages and take out the oldest message
        start = message_board[i][:43]       #
        end = message_board[i+1][43:]
        message_board[i] = start + end
    temp = message_board[len(message_board)-1][:43]
    message = temp + message
    message_board[len(message_board)-1] = message


if __name__ == '__main__':
    s = socket.socket()                                     #creating a socket object
    host = socket.gethostname()                             #get local machine name
    print(host)
    print(socket.gethostbyname(host))
    port = int(sys.argv[1])                                 #setting port to value user specifies 
    s.bind((host,port))                                     #bind to port
    message_board = [ "------------------------------\n" 
                    + f"Message #{i+1}:\n"
                    + "XXX XXX 00 00:00:00 0000 IP:0.0.0.0\n"
                    + "" for i in range(5)]                  #create empty message board 

    print("Do you want to clean received messages (y/n) ")  #ask user if they would like to clean messages
    if str(input()) == 'y':                                 # if y clean messages
        clean_messages(message_board)
    else:                                                   #else leave them alone
        print_messages(message_board)
    print(f"hostname: {host}, listening to port {port}")
    s.listen(5)

    while True: 
        print("Waiting for client...")
        c, addr = s.accept()                                # Establish connection with client.
        print("Connect to client!")
        
        message_encoded = c.recv(1024)                      # receive message from client
        print("Running decryption, please wait!")
        now = datetime.datetime.now()                       # check to see what time and where we got message from
        arrived = now.strftime("%a %b %d %H:%M:%S %Y IP: ") + addr[0] +"\n"  # create time and ip address string
        encrypted_message = message_encoded.decode()        # decode message from bits into string 
        message = decrpyt_message(encrypted_message)        # decrypt message
        result = arrived + message                          # create final message

        print("ReceiveData:")
        data = ""
        add_message(message_board, result)
        for x in message_board:
            data += x
            data += "\n"
            print(x)

        print("\nRunning encryption, please wait!") 
        data = encrypt_message(data)
        data_encoded = str.encode(data)
        print("Encryption completed")
        print("Send message to client.")
        c.send(data_encoded)
        c.close()                                           # Close the connection
   