# Online Stock Trading
 introductory program to socket interfaces and client/SSH-server applications

CIS 427

Project 1 - Online Stock Trading

Group 6: Taylor Williams, Michelle Sroka


Repository Link: https://github.com/mjensro/Online-Stock-Trading

Youtube Video Link:


                                    Operating Environment
Programming Language: Python

Operating system: Windows/Mac/Linux

SSH client for Windows: https://www.bitvise.com/ssh-client-download

Github Repository Link: https://github.com/mjensro/Online-Stock-Trading

Youtube Link:



                                    Commands Implemented

LOGIN- by Taylor Williams - Login the user to the remote server. A client that wants to login should begin by sending the ASCII string “LOGIN" followed by a space, followed by a UserID, followed by a space, followed by a Password, and followed by the newline character (i.e., '\n').


LOGOUT- by Taylor Williams - Logout from the server. A client sends the ASCII string “LOGOUT" followed by a name followed by the newline character (i.e., '\n'). A user is not allowed to send BUY, SELL, LIST, BALANCE, and SHUTDOWN commands after logout, but it can still send the QUIT commands. This command should result in the server terminating the allocated socket and thread for this client.


WHO- by Taylor Williams - List all active users, including the UserID and the user’s IP addresses. A client sends the ASCII string “WHO" followed by the newline character (i.e., '\n'). This command is only allowed for the root user.


LOOKUP- by Taylor Williams - Look up a stock name in the list. Display the complete stock record for the logged in user. A client sends the ASCII string “LOOKUP" followed by a space, followed by a name followed by the newline character (i.e., '\n'). 


DEPOSIT- by Michelle Sroka -Deposit USD to the user’s account/record. A user can deposit an amount of USD into their account. A client that wants to deposit an amount of USD should begin by sending the ASCII string “DEPOSIT" followed by a space, followed by a USD amount, followed by a space, followed the newline character (i.e., '\n'). 


BUY- by Michelle Sroka - Buy an amount of stocks. A client sends the ASCII string “BUY” followed by a space, followed by a stock_symbol, followed by a space, followed by a stock_amount, followed by
a space, followed by the price per stock, followed by a User_ID, and followed by the
newline character (i.e., '\n')


SELL- by Michelle Sroka - SELL an amount of stock. A client sends the ASCII string “BUY” followed by a space,followed by a stock_symbol, followed by a space, followed by stock price, followed by a
space, followed by a stock_amount, followed by a space, followed by a User_ID, and
followed by the newline character (i.e., '\n').


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

Login using ‘LOGIN “username” “password”’

Try using the following: WHO/LOOKUP/DEPOSIT/BUY/SELL/LIST/BALANCE/QUIT/SHUTDOWN/LOGOUT commands


                                    Testable Users
                                        UserID | Password 
                        
                                        Root   |  Root01 
                                        Mary   |  Mary01 
                                        John   |  John01 
                                        Moe    |  Moe01 
⠀

                                        Known Bugs

When the authorized user runs the SHUTDOWN command, the client side of the program exits with no issues but the server and other clients do not, even though its coded to do so. The function’s functionality was not changed from program 1 to program 2 so it could be a personal system error.



                                      Test Case Table

See ReadMe Doc.

                                        ScreenShots

See ReadMe Doc.