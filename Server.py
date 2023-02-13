#Author/Collaborators: Taylor Williams, Michelle Sroka, Alexis Whisnant
#Creation Date: 02/03/2023
#Last Modification Date: 02/12/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.

import socket
import sys
import sqlite3 #only server should handle SQL statements
from _thread import *

ip = ""
SERVER_PORT = 7399 #unique port using last 4 digits of ID
s = socket.socket (socket.AF_INET, socket.SOCK_STREAM) #Using transmission control protocol
db = sqlite3.connect("tables") #connection to SQLlite tables
dbActivity = db.cursor() #abstraction statement for data traversal

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

user = dbActivity.execute("SELECT ID FROM Users WHERE ID = 1") #checks if there is at least 1 user record
if user.fetchone() is None: #if no records exists, it creates 1 default
    dbActivity.execute("INSERT INTO USERS(ID, first_name, last_name, user_name, password, usd_balance) VALUES(1, 'User', '01', 'user1','password',100)")
    db.commit() #add changes to database
stockRecord = dbActivity.execute("SELECT ID FROM Stocks WHERE ID = 1") #checks if there is at least 1 stock record
if stockRecord.fetchone() is None: #Creates default stock records
    dbActivity.execute("INSERT INTO Stocks(ID, stock_symbol, stock_name, stock_balance, user_id) VALUES(1, 'TSLA', 'Tesla', '50.00','user1')")
    dbActivity.execute("INSERT INTO Stocks(ID, stock_symbol, stock_name, stock_balance, user_id) VALUES(2, 'AMZN', 'Amazon', '100.00','user1')")
    dbActivity.execute("INSERT INTO Stocks(ID, stock_symbol, stock_name, stock_balance, user_id) VALUES(3, 'MSFT', 'Microsoft', '250.00','user1')")
    db.commit()
try:
    #bind socket to a port on the s (local host)
    s.bind((ip,SERVER_PORT))
except socket.error as e:
    print(str(e))

#The queue of 1 for the s, if someone attempts to connect while
#queue is full they will be denied
print("Awaiting client connection...")
s.listen(1)

while True: #starting new thread
    #accepts new connection
    conn, addr = s.accept()
    print('connected to: '+addr[0]+':'+str(addr[1]))

    #recieves data stream and won't except data packet greater than 2048 bytes
    #convert to string format
    data = conn.recv(1024) #buffer rate
    data = data.decode("utf-8")
    print(data)
    """
    if not data:
        #if data is not recieved
        print("Data not recieved!")
        break

    """
    if len(data) == 0:
        #if invalid command format
        conn.send("403 message format error\n".encode())

    else:
        if (data == "SHUTDOWN"):
            print("it worked")
            conn.send(str.encode("200 OK"))
            conn.close()
            sys.exit()

        elif (data == "BALANCE"):#display the USD balance for user 1
            activeUserCheck = dbActivity.execute("SELECT * FROM Users WHERE ID = 1") #Selecting all information regarding user1 from Users table
            activeUser = activeUserCheck.fetchone()
            balanceMessage = "\nBalance for " + activeUser[1] + " " + activeUser[2] + ": $" + str(activeUser[5]) #displays users first and last name with their corresponding balance amount
            conn.send(balanceMessage.encode())

        elif (data == "LIST"):#List all records in the Stocks table/file
            stockActivity = dbActivity.execute("SELECT * FROM Stocks") #Finding all stock infromation within stock table
            stocks = stockActivity.fetchone() #fetch stock values
            list = "All records in the Stocks table: \n"
            while stocks is not None: #loop through all stock records within database
                list += str(stocks[0]) + " " +stocks[1] + " " + stocks[2] + " " + str(stocks[3]) + " " + stocks[4] + "\n"
                stocks = stockActivity.fetchone()
            conn.send(list.encode())

    conn.close()