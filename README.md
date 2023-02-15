# Online Stock Trading
 introductory program to socket interfaces and client/SSH-server applications

CIS 427

Project 1 - Online Stock Trading

Group 6: Taylor Williams, Michelle Sroka


Repository Link: https://github.com/mjensro/Online-Stock-Trading


                                    Operating Environment
Programming Language: Python

Operating system: Windows/Mac/Linux

SSH client for Windows: https://www.bitvise.com/ssh-client-download

                                    Commands Implemented

LIST- by Michelle Sroka - Displays all stock records within Stocks table

BALANCE- by Michelle Sroka - Shows balance for user 1

QUIT- by Taylor Williams - Upon user entering ‘QUIT’ the client is terminated

SHUTDOWN - by Taylor Williams - closes down all sockets and connection, then terminates

                                        How to compile

Download a secure shell application that will give you access to create a network communication protocol, such as the bitvise client. On Mac/Linux you may use the default terminal.


Sign into the following

Server Host: login.umd.umich.edu

Port: 22

Authenticate with personal username and password

Upload server, client, and sqlite table files via SFTP window

Open 2 new terminal windows and run the files by using the following commands:

    For server: python Server.py (run first)

    For client: python Client.py 127.0.0.1 (an example local ip address)
    
Wait for the client to connect to server

Test using LIST/BALANCE/QUIT/SHUTDOWN commands

