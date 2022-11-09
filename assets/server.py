import socket
from  threading import Thread
import time, random

SERVER = None
IP_ADDRESS = '127.0.0.1'
PORT = 8080

CLIENTS = {}
flashNumberList =[ i  for i in range(1, 91)]

gameOver = False
playersJoined = False



def handleClient():
    global CLIENTS
    global flashNumberList
    global gameOver
    global playersJoined

    while True:
        if(gameOver):
            break

        try:
            # Atleast two player required to play this game
            if(len(list(CLIENTS.keys())) >=2 and not gameOver):
                if(not playersJoined):
                    playersJoined = True
                    time.sleep(1)



                if(len(flashNumberList) > 0):
                    randomNumber = random.choice(flashNumberList)
                    currentName = None
                    try:
                        for cName in CLIENTS:
                            currentName = cName
                            cSocket = CLIENTS[cName]["playerSocket"]
                            cSocket.send(str(randomNumber).encode())

                        flashNumberList.remove(int(randomNumber))
                    except:
                        # Removing Player cleint when they close / terminate the session
                        del CLIENTS[currentName]

                    # After Every 3 Seconds we are sending one number to each CLIENT
                    time.sleep(3)
                else:
                    gameOver = True
        except:
            gameOver = True



def recvMessage(playerSocket):
    global CLIENTS
    global gameOver

    while True:
        try:
            message = playerSocket.recv(2048).decode()
            if(message):
                for cName in CLIENTS:
                    cSocket = CLIENTS[cName]["playerSocket"]
                    if('Wins the game!!!!!' in message):
                        gameOver = True
                    cSocket.send(message.encode())
        except:
            pass



def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        playerSocket, addr = SERVER.accept()
        playerName = playerSocket.recv(1024).decode().strip()

        CLIENTS[playerName] = {}
        CLIENTS[playerName]["playerSocket"] = playerSocket
        CLIENTS[playerName]["address"] = addr
        CLIENTS[playerName]["playerName"] = playerName

        print(f"Connection established with {playerName} : {addr}")

        thread1 = Thread(target = recvMessage, args=(playerSocket,))
        thread1.start()



def setup():
    print("\n\t\t\t\t\t*** Welcome To Tambola Game ***\n")

    global SERVER
    global PORT
    global IP_ADDRESS


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    thread = Thread(target = handleClient, args=())
    thread.start()


    acceptConnections()


setup()
