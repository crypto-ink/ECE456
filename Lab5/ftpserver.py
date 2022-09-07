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

def int_from_bytes(int_in_bytes):
    print("in int_fr")
    integer = int.from_bytes(int_in_bytes, 'big')
    print(integer)
    return integer   

def receive_stream(lisitning_socket, total_bytes, write_file):
    new_file = open(write_file, "wb")
    # stream = ""
    received = 1
    expected_packets = total_bytes/1024                     # calculate ammount of packets
    if (total_bytes % 1024 != 0):
        expected_packets += 1   
    while(received <= expected_packets):
        print(f"Receiving piece {received}")
        peice = lisitning_socket.recv(1024)
        new_file.write(peice)
        # stream += peice.decode()                            # add the text to string
        received += 1                                       # increment counter 
        lisitning_socket.send(str.encode("y"))                                     # let the sender know we are ready again
    
    new_file.close
    print("All pieces received!")
    print(f"File saved to {write_file}")
    return 

def clean_messages():
    return

def print_messages():
    return  

if __name__ == '__main__':
    s = socket.socket()                                     #creating a socket object
    host = socket.gethostname()                             #get local machine name
    port = int(sys.argv[1])                                 #setting port to value user specifies 
    s.bind((host,port))                                     #bind to port

    print("Do you want to clean received messages (y/n) ")  #ask user if they would like to clean messages
    if str(input()) == 'y':                                 # if y clean messages
        clean_messages()
    else:                                                   #else leave them alone
        print_messages()
    print(f"hostname: {host}, listening to port {port}")
    s.listen(5)

    while True: 
        print("Waiting for client...")
        c, addr = s.accept()                                # Establish connection with client.
        print("Connect to client!")
        stream = ""
        file_name_encoded = c.recv(1024)                    # receive the file name
        print("filename received ")
        byte_size_endoded = c.recv(1024)                    # receive the file size in bytes
        byte_size = int_from_bytes(byte_size_endoded)       # convert int in byte form to int
        print("file size received")
        print(f"Client {addr} requests to send a file, name: {file_name_encoded}, size: {byte_size}bytes")  #print address file name and file size
        print("Accept this file?{y/n)")                     # ask the user if they want to accept the file

        if str(input()) == 'y':
            print("Please rename received file:")
            file_renamed = input()
            c.send(str.encode('y'))                                     # prompt the client to send the files over
            receive_stream(c, byte_size, file_renamed)                       # receive the stream       
        else:
            c.send(str.encode('n'))                                     # tell the client the file was not accepted 
      
        c.close()                                           # Close the connection
        
        