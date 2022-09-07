import os
import socket               # Import socket module
import sys
import time
import datetime

def int_from_bytes(int_in_bytes):
    print(int_in_bytes)
    print("in int_from_bytes")
    integer = int.from_bytes(int_in_bytes, 'big')
    print(integer)
    return integer 

if __name__ == '__main__':
    s = socket.socket()                                     #creating a socket object
    host = socket.gethostname()                             #get local machine name
    port = int(sys.argv[1])                                 #setting port to value user specifies 
    s.bind((host,port))                                     #bind to port
    # print("hello World")
    print(f"hostname: {host}, listening to port {port}")

    print("------------------------------------------------------------")
    print("TCP remote command daemon")

    now = datetime.datetime.now()                       # check to see what time it is
    current_time = now.strftime("%a %b %d %H:%M:%S %Y") # create time 
    # Fri Feb 25 18:39:06 2022
    print(f"Current time: {current_time}")
    print(f"host: {host}")
    print(f"port: {port}")
    print("Status: closed\n")
    s.listen(5)                                         #start server listing to port

    while True:
        print("Wait for client...")                     #wait for client
        c, addr = s.accept()                            #when client attempts connection connect
        print("------------------------------------------------------------")
        print("Connected to client!")
        now = datetime.datetime.now()                   #find the time at the server
        current_time = now.strftime("%a %b %d %H:%M:%S %Y")
        print(f"Current time: {current_time}")          # print the current time at the server
        print(f"Source IP: {addr[0]}")                  # print the client IP

        command = c.recv(1024)                          # receive the command from the client
        c.send(str.encode('y'))                         # send confirmation that command was accepted
        exec_count = int(c.recv(1024).decode())         # receive the ammount of times to execute
        c.send(str.encode('y'))                         # send confirmation that command was accepted
        delay_time = int(c.recv(1024).decode())         # receive the delay_time
        # print(exec_count)
        # print(delay_time) 
        print(f"Command: {command}")                    #print command to be executed
        print("Status: connected")

        counter = 1                                     #create counter for time executed
        while counter <= exec_count:                    # check if we have executed the correct amount of time
            terminate_check = c.recv(1024).decode()     # receive wether or not we are terminating the current process
            if terminate_check == 'y':
                c.send(str.encode('y'))         #send confirmaton of current process being killed
                break                           #stop executing current process
            else:
                c.send(str.encode('n'))         #send cofirmation current process will continue
            
            now = datetime.datetime.now()       # find current time
            current_time = now.strftime("%a %b %d %H:%M:%S %Y")
            print(f"\nNo. {counter} execution: ")
            print(f"time of execution: {current_time}")
            print(f"execution time: ")
            print("Execution output: ")

            stream = os.popen(command.decode()) #popen() runs command and returns stream which was output to terminals
            output_raw = stream.readlines()     #gather all the info writter to terminal
            flow = os.popen(command.decode())   #open again but dont read
            output = ""                         #create a temp output
            for x in output_raw:                # add all of the output into output string
                output = output + x
            print(output)                       # print the command output
            c.send(str.encode(current_time))    # send the client the time command was executed at the server
            if len(output) > 1024:              # if len(output) > 1024 we will need to send pakcets
                packets = int(len(output) / 1024)   #calculate the ammount of packets   
                if len(output) % 1024 != 0:     #check if need to send another pakcet
                    packets += 1

                c.send(str.encode('y'))         #send that will need to accept more than one packet
                c.recv(1)                       #confirmed that will accept more than one packet
                c.send(str.encode(str(len(output))))    #send the ammount of bytes to expect

                packets_sent = 0                #create counter for packets sent
                while packets_sent < packets:   #while there are still packets to send
                    c.send(str.encode(flow.read(1024))) #send packet  
                    c.recv(1024)                #receive confirmation that the packet was received
                    packets_sent += 1           #increment packet counter
                    
            else:
                c.send(str.encode('n'))         #send notification that no more than 1 packet will be snet
                c.recv(1)                       #receive confirmation that ammount of packets was received
                c.send(str.encode(output))      #send the output from the command
                c.recv(1)                       #receive confirmation that output was sent
            print(f"Output Size: {len(output)} bytes")  
            time.sleep(delay_time)
            counter += 1 

        print("------------------------------------------------------------") 
        print("TCP remote command daemon")
        now = datetime.datetime.now()                       # check to see what time it is
        current_time = now.strftime("%a %b %d %H:%M:%S %Y") # create time 
        print(f"Current time: {current_time}")
        print(f"host: {host}")
        print(f"port: {port}")
        print("Status: closed\n")

        c.close()