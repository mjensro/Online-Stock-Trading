#Author/Collaborators: Taylor Williams, Michelle Sroka, Alexis Whisnant
#Creation Date: 02/03/2023
#Last Modification Date: 02/03/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.

import socket
import sys
import threading
import sqlite3
from _thread import *

ip = ''
SERVER_PORT = 7399 #last 4 digits of id for unique port
client_server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
client_server.connect((ip,port))

"""
#takes input
message = input("client:  ")

#Client chooses/inputs the SHUTDOWN command
if message == 'SHUTDOWN\n':
    #send message to server
    client_server.send(message.encode())
    
    #recieve response
    data = client_server.recv(2048).decode() 
     
    #Prints message recived from the server "200 OK"
    print(data)
    
    #return the string "200 OK"
    #reply = '200 OK'
    #print("client: " , reply)

    #end connection and terminate
    #client_server.close()
    """

if __name__ == "__main__":
    ip = ""
    n = len(sys.argv)
    if n == 2:
        print (sys.argv[1])
        host = sys.argv[1]
else:
    print ("Invalid argument")
    exit()

client_socket = socket.socket()

try:
    client_socket.connect((host,SERVER_PORT))
except:
    print("Cannot connect to server")
    exit()

shutDown = 0
while shutDown == 0: #while user does not request shutdown
    message = input("\ninput::") #accepting user input

    #quit message goes here
    
    if len(message) > 0:
        try:
            client_socket.send(message.encode()) #sending input to server
            data = client_socket.recv(1024).decode() #recieve sent input
            if data == "Shutting down server...":
                shutDown = 1
            print("Output: " + data) #outputting response
        except:
            print("lost connection to server")
            shutDown = 1

    client_socket.close() #close socket connection