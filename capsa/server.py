# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
import Queue
from Player import *
from Deck import *
from thread import *
import time
  
"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
# takes the first argument from command prompt as IP address 
IP_address = "192.168.1.8"
  
# takes second argument from command prompt as port number 
Port = 8080
  
""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, Port)) 
  
""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100) 
  
list_of_player = []
deck = generateCards()
player =[]
cards_on_board = []
turn = Queue.Queue()
first = 0

def setTurn():

    for i in range(len(player)):
        
        if player[i].conn != first:
            turn.put(player[i].conn)    


def chatThread(conn, addr): 

    while True: 
        pass
  
def broadcast(message): 
    for p in list_of_player:  
            try: 
                p.send(message) 
            except: 
                p.close() 
  
                remove(p)
    time.sleep(0.5)
  

def remove(connection): 
    if connection in list_of_player: 
        list_of_player.remove(connection) 


def getAllPlayers():
    while len(list_of_player) < 4:
        conn, addr = server.accept() 
        list_of_player.append(conn)

        print addr[0] + " connected "

        player.append(Player(addr[0], conn))
    
        player_cards =[]

        for i in range(13):
        
            if deck.empty():
                print "deck is empty\n\n"
                break

            card = deck.get()

            if card.value == 2 and card.type == 3:
                turn.put(conn)
                first = conn

            player_cards.append(card)

        conn.send("CARDS_"+"".join(str(card) for card in player_cards))
        player[-1].setCards(player_cards)
        
        time.sleep(0.5)

        # sends a message to the client whose user object is conn 
        message =  "NOTIFICATION_Welcome to CAPSA!\n\n"
    
        if len(player) < 4:
            message = message + "Waiting for " + str(4-len(player)) +" player to play this game\n\n"
        
        conn.send(message);
        start_new_thread(chatThread,(conn,addr))   


        


if __name__ == "__main__": 
    
    getAllPlayers()
    
    setTurn()
    
    Finish = False
    
    broadcast("NOTIFICATION_Lets Play!!!")

    playerNow = turn.get()
    turn.put(playerNow)


    while not Finish:
        playerNow.send("Play_Play")

        message = playerNow.recv(2048)
        while not message:
            message = playerNow.recv(2048)
        
        playerNow = turn.get()
        turn.put(playerNow)


server.close()