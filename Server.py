#Author/Collaborators: Taylor Williams, Michelle Sroka
#Creation Date: 02/03/2023
#Last Modification Date: 03/24/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.


import socket
import sys
import sqlite3 #only server should handle SQL statements
from _thread import *
import threading


#print_lock = threading.Lock()


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
    dbActivity.execute("INSERT INTO Users(ID, first_name, last_name, user_name, password, usd_balance) VALUES(1, 'User', 'Root', 'Root','Root01',100.00)")
    dbActivity.execute("INSERT INTO Users(ID, first_name, last_name, user_name, password, usd_balance) VALUES(2,'Mary','User','Mary','Mary01',100.00)")
    dbActivity.execute("INSERT INTO Users(ID, first_name, last_name, user_name, password, usd_balance) VALUES(3,'John','User','John','John01',100.00)")
    dbActivity.execute("INSERT INTO Users(ID, first_name, last_name, user_name, password, usd_balance) VALUES(4,'Moe','User','Moe','Moe01',100.00)")
    db.commit() #add changes to database
stockRecord = dbActivity.execute("SELECT ID FROM Stocks WHERE ID = 1") #checks if there is at least 1 stock record
if stockRecord.fetchone() is None: #Creates default stock records
    dbActivity.execute("INSERT INTO Stocks(ID, stock_symbol, stock_name, stock_balance, user_id) VALUES(1, 'TSLA', 'Tesla', '50.00','1')")
    dbActivity.execute("INSERT INTO Stocks(ID, stock_symbol, stock_name, stock_balance, user_id) VALUES(2, 'AMZN', 'Amazon', '100.00','1')")
    dbActivity.execute("INSERT INTO Stocks(ID, stock_symbol, stock_name, stock_balance, user_id) VALUES(3, 'MSFT', 'Microsoft', '250.00','2')")
    db.commit()
   
try:
    #bind socket to a port on the s (local host)
    s.bind((ip,SERVER_PORT))
except socket.error as e:
    print(str(e))


#The queue of 1 for the s, if someone attempts to connect while
#queue is full they will be denied
print("Awaiting client connection...")
s.listen(4)


while True: #starting new thread client connection
    #accepts new connection
    connection, address = s.accept()
    print('connected to: '+address[0]+':'+str(address[1]))


    #recieves data stream and won't except data packet greater than 2048 bytes
    #convert to string format
    data = connection.recv(1024).decode("utf-8") #buffer rate & decoding
    #data = data.decode("utf-8")
    #print(data)


    if len(data) == 0:
        #if invalid command format
        connection.send("403 message format error\n".encode())
        #print_lock.release()
        connection.close()
    

    """userID = dbActivity.execute("SELECT * FROM Users WHERE ID = 1") #Finds all user 01's information from users table
    validUser1= userID.fetchone() #fetch userID values
    validUser1 = validUser1[0] #the first valid user is identified by just their ID#


    userPassword = dbActivity.execute("SELECT * FROM Users WHERE password = 'password'") #Finds all user password information from users table
    validPassword1 = dbActivity.fetchone()#fetch user password values
    validPassword1 = validPassword1[4] #the first valid user's password"""

    userRequest = data.split(" ")
    data = userRequest[0]

    if (data ==  "LOGIN"): #for when the user's input is acccurate - LOGIN Mary Mary01 
        #command = userRequest[0] #grabs LOGIN command
        username = userRequest[1]
        password = userRequest[2]

        loggingIn = dbActivity.execute("SELECT ID FROM Users WHERE user_name = '" + username + "' AND password = '" + password + "'")
        logs = loggingIn.fetchone()
        if logs is None:
            connection.send("403 Wrong UserID or Password".encode())
            continue

        login = True
        loginMessage = "200 OK"
        connection.send(loginMessage.encode())


        while login == True: #starting new thread for valid client
            #lock acquired by client
            #print_lock.acquire()
            #connection.send(" inside client connection!".encode())


            #data sent from client
            clientdata = connection.recv(1024) #buffer rate
            clientdata = clientdata.decode("utf-8")
            print(clientdata)
       
            if (clientdata == "SHUTDOWN"):
                    #activeUser = activeUserCheck.fetchone()
                    #rootUser = activeUser[0]


                    #if the active user is the root user allow for shutdown
                    #if (validUser1 == rootUser):
                    sendMessage = "200 OK"
                    connection.send(sendMessage.encode()) #send message to client
                    connection.close()
                    sys.exit()
               
               
                    #connection.send("Only root user is authorized to SHUTDOWN! Denied!".encode())


            elif (clientdata == "BALANCE"):#display the USD balance for user 1
                    activeUserCheck = dbActivity.execute("SELECT * FROM Users WHERE user_name = '" + username + "'")
                    activeUser = activeUserCheck.fetchone()
                    balanceMessage = " 200 OK\n Balance for " + activeUser[1] + " " + activeUser[2] + ": $" + str(activeUser[5]) #displays users first and last name with their corresponding balance amount
                    connection.send(balanceMessage.encode())


            elif (clientdata == "LIST"):#List all records in the Stocks table/file
                    stockActivity = dbActivity.execute("SELECT * FROM Stocks") #Finding all stock infromation within stock table
                    stocks = stockActivity.fetchone() #fetch stock values
                    list = "200 OK \n The list of records in the Stocks database for user 1: "
                    while stocks is not None: #loop through all stock records within database
                        list += str(stocks[0]) + " " +stocks[1] + " " + stocks[2] + " " + str(stocks[3]) + " " + stocks[4] + "\n"
                        stocks = stockActivity.fetchone()
                    connection.send(list.encode())
            
            elif (data == "BUY"):
                    """
                    -have user enter the stock_symbol, stock_name, and the stock_balance amount they wish to purchase
                    -check if users usd_balance within Users table is enough to purchase stock amount
                        balance -= purchaseAmount
                    dbActivity.execute("INSERT INTO Stocks (stock_symbol, stock_name, stock_balance, user_id) VALUES ('" + stockSymbol + "','" + stockName + "','" + str(purchaseAmount) +"','user1')") 
                    """
                    userBalance = 0.0
                    if len(userRequest) < 4: #BUY MSFT 3.4 1.35 1 // Where 3.4 is the amount of stocks to buy, $1.35 price per stock, 1 is the user id.
                        connection.send("403 message format error".encode())
                        continue
                    stockName = userRequest[1]
                    amount = float(userRequest[2])
                    price = float(userRequest[3])
                    result = dbActivity.execute("SELECT usd_balance FROM USERS WHERE user_name = '" + username + "'")
                    temp = result.fetchone()
                    if temp is None:
                        connection.send("User not found".encode())
                        continue
                        
                    userBalance = temp[0]
                    if userBalance < 0:
                        connection.send("Not enough balance".encode())
                        continue
                    userBalance = float(userBalance - (amount * price)) #update balance value
                    result = dbActivity.execute("SELECT stock_balance FROM Stocks WHERE stock_name = '" + stockName + "' AND user_name = '" + username + "'")
                    temp = result.fetchone()
                    if temp is None:
                        dbActivity.execute("INSERT INTO Stocks (stock_name, stock_balance, user_id) VALUES ('" + stockName + "','" + str(amount) +"','" + username + "')") #if no crypto found, insert one
                        db.commit()
                    else:
                        oldAmount = temp[0]
                        amount += oldAmount
                        dbActivity.execute("UPDATE Stocks SET stock_balance = '" + str(amount) + "' WHERE user_name = '" + username + "' AND stock_name = '" + stockName + "'")
                        db.commit()
                        dbActivity.execute("UPDATE Users SET usd_balance = '" + str(userBalance) + "' WHERE user_name = '" + username + "'") #update balance in users account
                        db.commit()
                        result = dbActivity.execute("SELECT stock_balance FROM Stocks WHERE stock_name = '" + stockName + "' AND user_name = '" + username + "'")
                        stockBalance = result.fetchone()[0]
                        confirm = "200 OK \nBOUGHT: New balance: %.2f %s USD Balance: $%.2f" % (stockBalance, stockName, userBalance)
                        connection.send(confirm.encode())

            elif (data == "SELL"):
                        """-have user enter the stock_name, and the stock_balance they wish to sell
                        -verify user has the stock_name already purchased
                        dbActivity.execute("UPDATE Users SET usd_balance = '" + str(balance) +"'")
                        dbActivity.execute("INSERT INTO Stocks (stock_symbol, stock_name, stock_balance, user_id) VALUES ('" + stockSymbol + "','" + stockName + "','" + str(purchaseAmount) +"','user1')") """
                        userBalance = 0.0
                        oldAmount = 0.0
                        if len(userRequest) < 4: #SELL APPL 2 1.45 1 // Where stock symbol is APPL, amount to be sold 2, price per stock $1.45, and 1 is the userid.
                            connection.send("403 message format error".encode())
                            continue
                        stockName = userRequest[1]
                        amount = float(userRequest[2])
                        price = float(userRequest[3])
                        result = dbActivity.execute("SELECT usd_balance FROM USERS WHERE user_name = '" + username + "'")
                        temp = result.fetchone()
                        if temp is None:
                            connection.send("User not found".encode())
                            continue
                        else:
                            userBalance = temp[0]
                        result = dbActivity.execute("SELECT stock_balance FROM Stocks WHERE stock_name = '" + stockName + "' AND user_id = '" + username + "'")
                        temp = result.fetchone()
                        if temp is None:
                            connection.send("Stock record not found".encode())
                            continue
                        else:
                            oldAmount = temp[0]
                            
                        userBalance += float(amount * price)
                        amount = oldAmount - amount
                            
                        if amount < 0:
                            connection.send("Not enough stock balance".encode())
                            continue
                        dbActivity.execute("UPDATE Stocks SET stock_balance = '" + str(amount) + "' WHERE user_name = '" + username + "' AND stock_name = '" + stockName + "'")
                        db.commit()
                        dbActivity.execute("UPDATE USERS SET usd_balance = '" + str(userBalance) + "' WHERE user_name = '" + username + "'") #update balance in users account
                        db.commit()
                        result = dbActivity.execute("SELECT stock_balance FROM Stocks WHERE stock_name = '" + stockName + "' AND user_name = '" + username + "'")
                        stockBalance = result.fetchone()[0]
                        confirm = "200 OK\nSOLD: New balance: %s USD Balance: $" % (stockBalance,stockName, userBalance)
                        connection.send(confirm.encode())

    else: #If user enters invalid userID or password information
        connection.send("403 Wrong UserID or Password".encode())
        #print_lock.release()
        continue


    if (data == "SHUTDOWN"): #if user tries to enter shutdown without being logged in
        connection.send("Only root user is authorized to SHUTDOWN! Denied!".encode())


    connection.close()


