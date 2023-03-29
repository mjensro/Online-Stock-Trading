#Author/Collaborators: Taylor Williams, Michelle Sroka
#Creation Date: 02/03/2023
#Last Modification Date: 02/12/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.


import socket
import sys #used to input argv statements
from _thread import * #threading

#s = socket.socket()
#host = '127.0.0.1'
#port = 1233

SERVER_PORT = 7399 #last 4 digits of id for unique port
host = ""


s = socket.socket()


print('Waiting for connection')
try:
    s.connect((host, SERVER_PORT))
    print("Commands: \nLOGIN \nLIST \nLOGOUT \nWHO \nLOOKUP \nBUY \nSELL \nDEPOSIT \nBALANCE \nQUIT \nSHUTDOWN\n")
except socket.error as e:
    print(str(e))
    print("Cannot connect to server")



shutDown = 0
while shutDown == 0: #while user does not request shutdown
    userInput = raw_input("\ninput: ") #accepting user input


    if len(userInput) > 0:


        #quit message goes here
        if userInput == "QUIT":
          print("200 OK")
          s.close()


        if userInput == "SHUTDOWN":
          s.send(userInput.encode()) #sending input to server
          data = s.recv(1024).decode() #recieve sent input
          print("Output: " + data) #outputting response
          s.close()
          sys.exit()



        try:
            s.send(userInput.encode()) #sending input to server
            data = s.recv(1024).decode() #recieve sent input
            print("Output: " + data) #outputting response
           
        except:
            print("ERROR: Lost Connection")
            shutDown = 1
   
    else:
        print("Input handling went wrong! try restart client connection!")
       


s.close() #close socket connection
