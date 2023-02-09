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
    server.bind((ip,port)) 
except socket.error as e:
    print(str(e))

server.listen(5)
print('Waiting for connection...')

def threaded_client(conn):
    conn.send(str.encode('Welcome, type your info\n'))

    while True: #keeps thread active as long as the user doesn't exit
        data = conn.recv(2048) #buffer rate
        reply = 'Server output: '+ data.decode('utf-8')
        if not data:
            break
        conn.sendall(str.encode(reply))
    conn.close()

while True: #starting new thread
    conn, addr = server.accept()
    print('connected to: '+addr[0]+':'+str(addr[1]))
    
    start_new_thread(threaded_client,(conn,))
#client, address = server.accept()
#print(f"Connection Established -  {address[0]}:{address[1]}")

#print("Client Disconnected")