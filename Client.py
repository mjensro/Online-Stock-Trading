#Author/Collaborators: Taylor Williams, Michelle Sroka
#Creation Date: 02/03/2023
#Last Modification Date: 02/12/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.


import socket #used to connect to socket
import sys #used to input argv statements
from _thread import * #threading


SERVER_PORT = 7399 #last 4 digits of id for unique port


if __name__ == "__main__":
    host = ""
    n = len(sys.argv) #intakes compiling statement as an array
    if n == 2: #if the input recieves an ip
        host = sys.argv[1]
        print (host) #print ip inputted
else:
    print ("Invalid argument")
    exit()




s = socket.socket()


try:
    s.connect((host,SERVER_PORT)) #connect to host given with pre-assigned port number
    print("Commands: \nLOGIN \nLIST \nLOGOUT \nWHO \nLOOKUP \nBALANCE \nQUIT \nSHUTDOWN\n")
except:
    print("Cannot connect to server")
    exit()




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

