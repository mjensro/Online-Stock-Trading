#Author/Collaborators: Taylor Williams, Michelle Sroka, Alexis Whisnant
#Creation Date: 02/03/2023
#Last Modification Date: 02/03/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.

#Following this tutorial : https://www.youtube.com/watch?v=6sHGBXwkFQU
import socket
import sys

ip = ''
port = 7399 #last 4 digits of id for unique port
server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip,port))


#if __name__ == "__main__":
