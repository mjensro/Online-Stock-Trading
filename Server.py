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

ip = ""
SERVER_PORT = 7399
server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
db = sqlite3.connect("tables.sqlite",check_same_thread=False) #connection to SQLlite tables
dbActivity = db.cursor()

try:
    #bind socket to a port on the server (local host)
    server.bind((ip,SERVER_PORT))
except socket.error as e:
    print(str(e))


#The queue of 1 for the server, if someone attempts to connect while
#queue is full they will be denied
server.listen(1)


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

    elif (data == "BALANCE"):#display the USD balance for user 1
        activeUser = dbActivity.execute("SELECT first_name, last_name, usd_balance FROM Users WHERE user_name = 'user1'") #Selecting all information regarding user1 from Users table

        if activeUser.fetchone() is None: #if there are no users within database
            dbActivity.execute("INSERT INTO USERS(email, first_name,last_name,user_name,password,usd_balance) VALUES('user1@gmail.com', 'User', '1', 'user1','user01',100)")
            db.commit() #accepting changes made to database

        balanceMessage = "\nBalance for " + activeUser[0] + " " + activeUser[1] + ": $" + str[activeUser[2]] #displays users first and last name and balance amount
        conn.send(balanceMessage.encode())

    elif (data == "LIST"):#List all records in the Stocks table/file
        stockActivity = dbActivity.execute("SELECT usd_balance FROM USERS WHERE ID = 1") #Finding user 1

        if stockActivity.fetchone() is None: #if there are no current stock records within database
            dbActivity.execute("INSERT INTO Stocks(ID, stock_symbol, stock_name, stock_balance, user_id) VALUES(2, 'TSLA', 'Tesla', '50','user1')")
            db.commit()
        
        listMessage = "\nComplete list of records within the Stocks Table:"
        stockActivity = dbActivity.execute("Select ID, stock_symbol, stock_name, stock_balance, user_id from Stocks")
        stocks = stockActivity.fetchone()

        conn.send(listMessage.encode())

        while stocks is not None:
            listMessage += "\n" + str(stocks[0]) + " " + stocks[1] + " " + str(stocks[2])

    conn.close()


#if __name__ == '__main__':