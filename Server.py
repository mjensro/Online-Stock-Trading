#Author/Collaborators: Taylor Williams, Michelle Sroka, Alexis Whisnant
#Creation Date: 02/03/2023
#Last Modification Date: 02/03/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.

import socket
import sys
from _thread import *

#if __name__ == "__main__":

ip = "127.0.0.1"
port = 7399
server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)


try:
    #bind socket to a port on the server (local host)
    server.bind((ip,port))
except socket.error as e:
    print(str(e))


#The queue of 1 for the server, if someone attempts to connect while
#queue is full they will be denied
server.listen(1)

print('Waiting for connection...')

while True: #starting new thread
    #accepts new connection
    conn, addr = server.accept()
    print('connected to: '+addr[0]+':'+str(addr[1]))

    #conn.send('Welcome, type your info\n'.encode())

    #recieves data stream and won't except data packet greater than 2048 bytes
    data = conn.recv(2048) #buffer rate

    if not data:
        #if data is not recieved
        break

    #prints what the client sent to the server
    print("Recieved: ", + str(data))

    if(data == "SHUTDOWN\n"):
      reply = 'server: '+ data.decode('200 OK')
      #sends data to the client
      conn.sendall(str.encode(reply))
      #end connection and terminate
      conn.close()


    #conn.close()