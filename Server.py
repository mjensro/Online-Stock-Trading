#Author/Collaborators: Taylor Williams, Michelle Sroka
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
INSERT INTO Users (ID, first_name, last_name, user_name, password, usd_balance)
VALUES('01','Root','User','Root','Root01',100),
VALUES('02','Mary','User','Mary','Mary01',100),
VALUES('03','John','User','John','John01',100),
VALUES('04','Moe','User','Moe','Moe01',100);
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
    connection, address = s.accept()
    print('connected to: '+address[0]+':'+str(address[1]))

    #recieves data stream and won't except data packet greater than 2048 bytes
    #convert to string format
    data = connection.recv(1024) #buffer rate
    data = data.decode("utf-8")
    print(data)

    if len(data) == 0:
        #if invalid command format
        connection.send("403 message format error\n".encode())

    else:
        userID = dbActivity.execute("SELECT ID * FROM Users") #Finds all user ID information from user table
        validUser = userID.fetchone() #fetch userID values
        if (data == "LOGIN " + validUser + " "):




        elif (data == "SHUTDOWN"):
            sendMessage = "200 OK"
            connection.send(sendMessage.encode()) #send message to client
            connection.close()
            sys.exit()

        elif (data == "BALANCE"):#display the USD balance for user 1
            activeUserCheck = dbActivity.execute("SELECT * FROM Users WHERE user_name = 'user1'") #Selecting all information regarding user1 from Users table
            activeUser = activeUserCheck.fetchone()
            balanceMessage = " 200 OK\n Balance for " + activeUser[1] + " " + activeUser[2] + ": $" + str(activeUser[5]) #displays users first and last name with their corresponding balance amount
            connection.send(balanceMessage.encode())

        elif (data == "LIST"):#List all records in the Stocks table/file
            stockActivity = dbActivity.execute("SELECT * FROM Stocks") #Finding all stock infromation within stock table
            stocks = stockActivity.fetchone() #fetch stock values
            list = "200 OK \n The list of records in the Stocks database for user 1: \n"
            while stocks is not None: #loop through all stock records within database
                list += str(stocks[0]) + " " +stocks[1] + " " + stocks[2] + " " + str(stocks[3]) + " " + stocks[4] + "\n"
                stocks = stockActivity.fetchone()
            connection.send(list.encode())

        #elif (data == "BUY"):
            """
            -have user enter the stock_symbol, stock_name, and the stock_balance amount they wish to purchase
            -check if users usd_balance within Users table is enough to purchase stock amount
            -subtract usd_balance by buy amount as long as user will not have negative funds remaining
            -update stock table with new stock_symbol, stock_name
            -return new usd_balance
            """
            """
            stockName = input("Enter Stock Name")
            stockSymbol = input("Enter Stock Symbol")
            purchaseAmount = input("Enter amount to purchase:")
            userBalance = dbActivity.execute("SELECT usd_balance FROM Users WHERE user_name = 'user1'")
            balance = userBalance.fetchone()
            if balance > purchaseAmount:
                print("insufficient funds")
            else:
                 balance -= purchaseAmount
            dbActivity.execute("INSERT INTO Stocks (stock_symbol, stock_name, stock_balance, user_id) VALUES ('" + stockSymbol + "','" + stockName + "','" + str(purchaseAmount) +"','user1')") 
            """
        #elif (data == "SELL"):
            """
            -have user enter the stock_name, and the stock_balance they wish to sell
            -verify user has the stock_name already purchased
            -add stock_balance to users usd_balance, update usd_balance
            -update Stock table with removed stock record
            -return new usd_balance
            """
            """
            stockName = input("Enter Stock Name: ")
            stockSymbol = input("Enter Stock Symbol: ")
            purchaseAmount = input("Enter amount to sell: ")
            userBalance = dbActivity.execute("SELECT usd_balance FROM Users WHERE user_name = 'user1'")
            balance = userBalance.fetchone()
            balance += purchaseAmount
            dbActivity.execute("UPDATE Users SET usd_balance = '" + str(balance) +"'")
            dbActivity.execute("INSERT INTO Stocks (stock_symbol, stock_name, stock_balance, user_id) VALUES ('" + stockSymbol + "','" + stockName + "','" + str(purchaseAmount) +"','user1')") 
            """
    connection.close()