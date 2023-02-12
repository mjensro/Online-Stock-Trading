#Author/Collaborators: Taylor Williams, Michelle Sroka, Alexis Whisnant
#Creation Date: 02/03/2023
#Last Modification Date: 02/03/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the s.

import socket
import sys
import threading
import sqlite3
from _thread import *

ip = ""
SERVER_PORT = 7390
s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
db = sqlite3.connect("tables") #connection to SQLlite tables
dbActivity = db.cursor()

#User table creation
dbActivity.execute("""
CREATE TABLE IF NOT EXISTS Users
(
    ID INTEGER PRIMARY KEY, 
    first_name TEXT,
    last_name TEXT,
    user_name TEXT NOT NULL,
    password TEXT,         
    usd_balance DOUBLE NOT NULL
);
""")

#Stock table creation
dbActivity.execute("""
CREATE TABLE IF NOT EXISTS Stocks
(
    ID INTEGER PRIMARY KEY,

    stock_symbol varchar(4) NOT NULL,
    stock_name varchar(20) NOT NULL,
    stock_balance DOUBLE,
    user_id TEXT,        
    FOREIGN KEY (user_id) REFERENCES Users (ID)           
);
""")

user = dbActivity.execute("SELECT ID FROM Users WHERE ID = 1")
if user.fetchone() is None:
    dbActivity.execute("INSERT INTO USERS(ID, first_name, last_name, user_name, password, usd_balance) VALUES(1, 'User', '01', 'user1','password',100)")
    db.commit()
stockRecord = dbActivity.execute("SELECT ID FROM Stocks WHERE ID = 1")
if stockRecord.fetchone() is None:
    dbActivity.execute("INSERT INTO Stocks(ID, stock_symbol, stock_name, stock_balance, user_id) VALUES(1, 'TSLA', 'Tesla', '50','user1')")
    db.commit()
try:
    #bind socket to a port on the s (local host)
    s.bind((ip,SERVER_PORT))
except socket.error as e:
    print(str(e))

#The queue of 1 for the s, if someone attempts to connect while
#queue is full they will be denied
s.listen(1)

while True: #starting new thread
    #accepts new connection
    conn, addr = s.accept()
    print('connected to: '+addr[0]+':'+str(addr[1]))

    #conn.send('Welcome, type your info\n'.encode())

    #recieves data stream and won't except data packet greater than 2048 bytes
    #convert to string format
    data = conn.recv(1024) #buffer rate
    data = data.decode("utf-8")
    print(data)

    """""
    if not data:
        #if data is not recieved
        print("Data not recieved!")
        break

    """""

    if len(data) == 0:
        #if invalid command format
        conn.send("403 message format error\n".encode())

    #prints what the client sent to the s
    #print("Recieved: ", + str(data))
    
    else:
        
        if (data == "SHUTDOWN"):
            print("it worked")
            conn.send(str.encode("200 OK"))
            conn.close()
            sys.exit()

    
        elif (data == "BALANCE"):#display the USD balance for user 1
            activeUserCheck = dbActivity.execute("SELECT ID, first_name, last_name, user_name, password, usd_balance FROM Users WHERE ID = 1") #Selecting all information regarding user1 from Users table
            activeUser = activeUserCheck.fetchone()
            """if activeUser.fetchone() is None: #if there are no users within database
                dbActivity.execute("INSERT INTO USERS(ID, first_name, last_name, user_name, password, usd_balance) VALUES(1, 'User', '01', 'user1','password',100)")
                
                db.commit() #accepting changes made to database"""
                #activeUser = dbActivity.execute("SELECT ID, first_name, last_name, user_name, password, usd_balance FROM Users WHERE ID = 1") #Selecting all information regarding user1 from Users table

            balanceMessage = "\nBalance for " + activeUser[1] + " " + activeUser[2] + ": $" + str(activeUser[5]) #displays users first and last name and balance amount
            conn.send(balanceMessage.encode())

        elif (data == "LIST"):#List all records in the Stocks table/file
            stockActivity = dbActivity.execute("SELECT * FROM Stocks") #Finding user 1
            stocks = stockActivity.fetchone()
            while stocks is not None:
                list = "All records in the Stocks table: " + str(stocks[0]) + " " +stocks[1] + " " + stocks[2] + " " + str(stocks[3]) + " " + stocks[4]
                stocks = stockActivity.fetchone()
            """if stockActivity.fetchone() is None: #if there are no current stock records within database
                dbActivity.execute("INSERT INTO Stocks(ID, stock_symbol, stock_name, stock_balance, user_id) VALUES(1, 'TSLA', 'Tesla', '50','user1')")
                db.commit()"""
            
         #   stockActivity = dbActivity.execute("Select ID, stock_symbol, stock_name, stock_balance, user_id from Stocks")
            #stocks = stockActivity.fetchone()

            conn.send(list.encode())

           # while stocks is not None:
             #   listMessage += "\n" + str(stocks[0]) + " " + stocks[1] + " " + str(stocks[2])

    conn.close()