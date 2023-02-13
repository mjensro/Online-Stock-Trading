#Author/Collaborators: Taylor Williams, Michelle Sroka, Alexis Whisnant
#Creation Date: 02/03/2023
#Last Modification Date: 02/12/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.

import socket
import sys
from _thread import *

SERVER_PORT = 7399 #last 4 digits of id for unique port

if __name__ == "__main__":
    host = ""
    n = len(sys.argv) #intakes compiling statement as an array
    if n == 2: #if the input recieves an ip
        print (sys.argv[1]) #print ip inputted
        host = sys.argv[1]
else:
    print ("Invalid argument")
    exit()

s = socket.socket()

try:
    s.connect((host,SERVER_PORT)) #connect to host given with pre-assigned port number
    print("Commands: \nBUY \nSELL \nLIST \nBALANCE \nQUIT \nSHUTDOWN\n")
except:
    print("Cannot connect to server")
    exit()


shutDown = 0
while shutDown == 0: #while user does not request shutdown
    userInput = raw_input("input: ") #accepting user input

    #quit message goes here
    if userInput == "QUIT":
        print("200 OK")
        s.close()

    if len(userInput) > 0:
        try:
            s.send(userInput.encode()) #sending input to server
            data = s.recv(1024).decode() #recieve sent input
            print("Output: " + data) #outputting response
        except:
            print("lost connection to server")
            shutDown = 1

    s.close() #close socket connection