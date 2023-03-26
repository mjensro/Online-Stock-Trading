#Author/Collaborators: Taylor Williams, Michelle Sroka
#Creation Date: 02/03/2023
#Last Modification Date: 03/26/2023
#Purpose: This is the Server program for a Online Stock Trading System. This Server program is
#expected to communicate with an aligining Client program using TCP sockets. One active
#client should be allowed to connect to the server.


import socket
import sys
import sqlite3 #only server should handle SQL statements
from _thread import *
import threading

#print_lock = threading.Lock()  #for multi-threading clients

clientNames = [] 
clientAddresses = []

#MAIN
ip = ""
SERVER_PORT = 7399 #unique port using last 4 digits of ID
s = socket.socket (socket.AF_INET, socket.SOCK_STREAM) #Using transmission control protocol
db = sqlite3.connect("tables", check_same_thread=False) #connection to SQLlite tables
dbActivity = db.cursor() #abstraction statement for data traversal



#User table creation
dbActivity.execute("""
CREATE TABLE IF NOT EXISTS "Users"
(
    "ID" INTEGER PRIMARY KEY,
    "first_name" TEXT,
    "last_name" TEXT,
    "user_name" TEXT NOT NULL,
    "password" TEXT NOT NULL,        
    "usd_balance" DOUBLE NOT NULL
);
""")


#Stock table creation
dbActivity.execute("""
CREATE TABLE IF NOT EXISTS "Stocks"
(
    "ID" INTEGER PRIMARY KEY,
    "stock_symbol" varchar(4) NOT NULL,
    "stock_name" varchar(20) NOT NULL,
    "stock_balance" DOUBLE,
    "user_id" TEXT,        
    FOREIGN KEY ("user_id") REFERENCES "Users" ("ID")          
);
""")


user = dbActivity.execute("SELECT ID FROM Users WHERE ID = 1") #checks if there is at least 1 user record
if user.fetchone() is None: #if no records exists, it creates 1 default
    dbActivity.execute("INSERT INTO Users(ID, first_name, last_name, user_name, password, usd_balance) VALUES(1,'User', 'Root', 'root','root01',100.00)")
    dbActivity.execute("INSERT INTO Users(ID, first_name, last_name, user_name, password, usd_balance) VALUES(2,'Mary','User','mary','mary01',100.00)")
    dbActivity.execute("INSERT INTO Users(ID, first_name, last_name, user_name, password, usd_balance) VALUES(3,'John','User','john','john01',100.00)")
    dbActivity.execute("INSERT INTO Users(ID, first_name, last_name, user_name, password, usd_balance) VALUES(4,'Moe','User','moe','moe01',100.00)")
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


#a forever loop until client wants to exit
while True:
    #accepts new connection
    connection, address = s.accept()
    print('connected to: '+address[0]+':'+str(address[1]))
    #lock acquired by client
    #print_lock.acquire()
    
    #start_new_thread(threaded_client(connection,))
    #THREADED CLIENT LOOP
    while True:
        data = connection.recv(1024).decode()#"utf-8") #buffer rate & decoding
        print(data)
        
        if not data:
            #lock released on exit
            #print_lock.release()
            break
        #data = data.decode("utf-8")

        userRequest = data.split(" ")
        command = userRequest[0]

        if (command ==  "LOGIN"): #for when the user's input is acccurate - LOGIN mary mary01 
            #command = userRequest[0] #grabs LOGIN command
            username = userRequest[1] #intakes username if inputted correctly
            password = userRequest[2] #intakes password if inputted correctly

            clientNames.append(username) #adds client to list on connection
            clientAddresses.append(address[0]+':'+str(address[1])) #adds client address to list on connection
                        

            if len(userRequest) < 3: #checks for proper formatting and values for the BUY command
                connection.send("403 message format error".encode())
                continue

            result = dbActivity.execute("SELECT * FROM Users WHERE user_name = '" + username +"' AND password = '" + password +"'")
            #logs = loggingIn.fetchone() #fetching a user if an existing username and password was entered
            temp = result.fetchone()

            if temp is None: #if no ID exists for the inputted username & password - send error
                connection.send("403 Wrong UserID or Password".encode())
                login = False
                continue


            elif temp is not None:
                login = True
                loginMessage = "200 OK"
                connection.send(loginMessage.encode())
                #username = logs[3]
                #userID = logs[0]


            while login == True: #starting new thread for valid client
                    #lock acquired by client
                    #print_lock.acquire()
            
                    #data sent from client
                    clientdata = connection.recv(1024) #buffer rate
                    clientdata = clientdata.decode("utf-8")
                    print(clientdata)
                    #put above three lines out of this loop for logout function to work

                    #FUNCTION FOR LOGOUT
                    if(clientdata == "LOGOUT"):
                         connection.send("200 OK".encode())
                         connection.close()

                         #A user is not allowed to send BUY, SELL, LIST, BALANCE, and SHUTDOWN commands after logout, 
                         # but it can still send the QUIT commands.
                         


                    #FUNCTION FOR WHO
                    #checks if client login info matches the root user for authorization, then displays all users connected
                    if (clientdata == "WHO"):
                        if (username == "root" and password == "root01"):
                            activeuserList = "200 OK\n The list of the active users:\n"
                            #while the user and addresses(s) lists contain values
                            for n in clientNames:
                                for a in clientAddresses :
                                #display all active users of connection
                                    activeuserList += str(n) + "  " + str(a)
                            connection.send(activeuserList.encode())
                        
                        else:
                            connection.send("Error! Only Root User is authorized to use command : 'WHO', try another command.".encode())
                            continue #might need to take this ou

                    #FUNCTION FOR SHUTDOWN - ONLY ROOT USER IS AUTHORIZED
                    if (clientdata == "SHUTDOWN"):
                            if (username == "root" and password == "root01"):
                                #if the active user is the root user allow for shutdown
                                sendMessage = "200 OK"
                                connection.send(sendMessage.encode()) #send message to client
                                connection.close()
                                sys.exit()

                            else:
                                connection.send("Only root user is authorized to SHUTDOWN! Denied!".encode())
                                continue

                    
                    elif (clientdata == "BALANCE"):#display the USD balance for user 1
                            activeUserCheck = dbActivity.execute("SELECT * FROM Users WHERE user_name = '" + username + "'")
                            activeUser = activeUserCheck.fetchone()
                            balanceMessage = " 200 OK\n Balance for " + activeUser[1] + " " + activeUser[2] + ": $" + str(activeUser[5]) #displays users first and last name with their corresponding balance amount
                            connection.send(balanceMessage.encode())


                    elif (clientdata == "LIST"):#List all records in the Stocks table/file
                            stockActivity = dbActivity.execute("SELECT * FROM Stocks") #Finding all stock infromation within stock table
                            stocks = stockActivity.fetchone() #fetch stock values
                            list = "200 OK \n The list of records in the Stocks database for " + username
                            while stocks is not None: #loop through all stock records within database
                                list += str(stocks[0]) + " " +stocks[1] + " " + stocks[2] + " " + str(stocks[3]) + " " + stocks[4] + "\n"
                                stocks = stockActivity.fetchone()
                            connection.send(list.encode())
                    
                    elif (command == "BUY"):
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
                                dbActivity.execute("INSERT INTO Stocks (stock_symbol, stock_name, stock_balance, user_id) VALUES ('" + stockName + "','" + stockName + "','" + str(amount) +"','" + username + "')") #inserts stock record if one doesn't already exist
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

            
            if (command == "SHUTDOWN"): #if user tries to enter shutdown without being logged in
                connection.send("Only root user is authorized to SHUTDOWN! Denied!".encode())
           
            #If the user is not logged in yet, and they try a command other than, shutdown(not authorized), login, or quit(client operation)
            if (command != "LOGIN" or "QUIT"):
                 connection.send("This command is not allowed! Make sure you are logged into the server first!".encode())
                 

            else: #If user enters invalid userID or password information
                connection.send("403 Wrong UserID or Password123".encode())
                #print_lock.release()
                #continue

        

    connection.close() 


