#Author/Collaborators: Taylor Williams, Michelle Sroka, Alexis Whisnant
#Creation Date: 02/03/2023
#Last Modification Date: 02/03/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.

import socket
import sys
from _thread import *

#ip = ''
SERVER_PORT = 7399 #last 4 digits of id for unique port
#s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
#s.connect((ip,SERVER_PORT))

if __name__ == "__main__":
    ip = ""
    n = len(sys.argv)
    if n == 2:
        print (sys.argv[1])
        host = sys.argv[1]
else:
    print ("Invalid argument")
    exit()

s = socket.socket()

try:
    s.connect((ip,SERVER_PORT)) #changed host to ip
except:
    print("Cannot connect to server")
    exit()


shutDown = 0
while shutDown == 0: #while user does not request shutdown
    message = raw_input("input: ") #accepting user input

    #quit message goes here
    if message == "QUIT":
        print("200 OK")
        s.close()

    if len(message) > 0:
        try:
            s.send(message.encode()) #sending input to server
            data = s.recv(1024).decode() #recieve sent input
            print("Output: " + data) #outputting response
        except:
            print("lost connection to server")
            shutDown = 1

    s.close() #close socket connection