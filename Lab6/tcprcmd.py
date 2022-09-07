from gc import DEBUG_LEAK
import os 
import socket
import sys
import threading
import time

terminate = False

def thread_client(host, port, exec_count, delay_time, command):
    print("Your input:")                    #print what the socket thread was given
    print(f"host: {host}")
    print(f"port: {port}")
    print(f"execution count: {exec_count}")
    print(f"delay time: {delay_time}")
    print(f"command: {command}")
    s = socket.socket()  
    s.connect((host, port))
    s.send(str.encode(command))     #send the server the command
    s.recv(1)
    s.send(str.encode(exec_count))  #send the time to execute
    s.recv(1)
    s.send(str.encode(delay_time))  #send the delay time 

    counter = 1
    while counter <= int(exec_count):
        if(terminate):                              #check if we are terminating thread
            # print("breaking thread")                #announce thread is being killed
            s.send(str.encode('y'))                 #tell the server to kill current process
            s.recv(1024)                            #receive confirmation that breaking was received
            break                                   #break communicain with server
        else:
            s.send(str.encode('n'))                 #tell server to continue
            s.recv(1024)                            #receive confirmation that breaking was received
        print(f'\nNo. {counter} execution:')        #notify which execution we are on
        time_server = s.recv(1024).decode()         #receive the time which the command was executed on server
        print(f"Time at server: {time_server}")     #print time at server
        print("Output:")
        ftp_protocol = s.recv(1024).decode()        #receive if we will need to receive more than one packet
        if ftp_protocol == 'y':                     #we need to receive more than one packet
            output = ""                             #dummy variable for the output to fill
            s.send(str.encode('y'))                 #send confirmation that we will accept more than 1 packet
            length = int(s.recv(1024).decode())     #length of message in bytes
            packets = int(length / 1024)            #calculate the ammount of packets given
            packets_received = 0                    #create counter for ammount of packet received
            if length % 1024 != 0:                  #if there is a remainder we need one more packet
                packets += 1
            while packets_received < packets:       # while we have been given less packets keep receiving packets
                output = output + s.recv(1024).decode() #receive part of the output and add it to output
                s.send(str.encode('y'))             # send confirmation that packet was received
                packets_received += 1               # increment packet counter
        else:
            s.send(str.encode('y'))                 #sending confirmation that no more than x packets will be sent
            output = s.recv(1024).decode()          #receiving the output to print
            s.send(str.encode('y'))                 #sending confirmation that output was received


        print(output)                               #print output from server
        time.sleep(int(delay_time))                 #wait set ammount of time until next execution
        counter += 1                                #increase execution counter

    s.close()                                       #close connection with server
    print("All work has been done.")
    print("Session is terminated.")



if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    exec_count = sys.argv[3]
    delay_time = sys.argv[4]
    command = sys.argv[5]
    kill_process = False

    x = threading.Thread(target = thread_client, args= (host, port, exec_count, delay_time, command), daemon= True)
    x.start()
    user_input = input()
    if user_input == "rcend":
        print(f"user input: {user_input}")
        terminate = True
    else:
        print(f"user input: {user_input}")
    x.join()


# import os
# import socket
# from struct import pack               # Import socket module
# import time
# import sys


# if __name__ == '__main__':
#     host = sys.argv[1]
#     port = int(sys.argv[2])
#     exec_count = sys.argv[3]
#     delay_time = sys.argv[4]
#     command = sys.argv[5]
#     print("Your input:")
#     print(f"host: {host}")
#     print(f"port: {port}")
#     print(f"execution count: {exec_count}")
#     print(f"delay time: {delay_time}")
#     print(f"command: {command}")

#     s = socket.socket()  
#     s.connect((host, port))
#     s.send(str.encode(command))     #send the server the command
#     s.recv(1)
#     s.send(str.encode(exec_count))  #send the time to execute
#     s.recv(1)
#     s.send(str.encode(delay_time))  #send the delay time 

#     counter = 1
#     while counter <= int(exec_count):
#         print(f'\nNo. {counter} execution:')
#         time_server = s.recv(1024).decode()
#         print(f"Time at server: {time_server}")
#         print("Output:")
#         ftp_protocol = s.recv(1024).decode()
#         if ftp_protocol == 'y':
#             output = ""
#             # print("to be implemented")
#             s.send(str.encode('y'))
#             length = int(s.recv(1024).decode())
#             # print(length)
#             packets = int(length / 1024)
#             packets_received = 0
#             if length % 1024 != 0:
#                 packets += 1
#             # print(packets)
#             while packets_received < packets:
#                 # print(f"receiving packets {packets_received}")
#                 # print(output)
#                 output = output + s.recv(1024).decode()
#                 s.send(str.encode('y'))
#                 # print("sent confermation")
#                 packets_received += 1
#         else:
#             s.send(str.encode('y'))
#             output = s.recv(1024).decode()
#             s.send(str.encode('y'))
#         print(output)
#         time.sleep(int(delay_time))
#         counter += 1

#     print("All work has been done.")
#     print("Session is terminated.")
#     s.close()

