# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
import Queue
import pickle
from Player import *
from Deck import *
from Message import *
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

    for conn in list_of_player:
        
        if conn != first:
            turn.put(conn)    


def chatThread(conn, addr): 

    while True: 
        pass
  
def broadcast(message): 
    for p in list_of_player:  
            try: 
                p.send(pickle.dumps(message)) 
            except: 
                p.close() 
  
                remove(p)
    time.sleep(0.5)
  

def remove(connection): 
    if connection in list_of_player: 
        list_of_player.remove(connection) 


def getAllPlayers():
    while len(list_of_player) < 400:
        conn, addr = server.accept() 
        list_of_player.append(conn)
        global first
        print addr[0] + " connected "

        player.append(Player(addr[0]))
    
        player_cards =[]

        for i in range(13):
        
            if deck.empty():
                print "deck is empty\n\n"
                break

            card = deck.get()

            if card.number == 2 and card.type == 3:
                turn.put(conn)
                first = conn

            player_cards.append(card)
        
        player[-1].setCards(player_cards)
        
        conn.send(pickle.dumps(Message("PLAYER",player[-1])))
        time.sleep(2)
        # sends a message to the client whose user object is conn 
        message =  Message("NOTIFICATION","Welcome to CAPSA!\n\n");
    
        if len(player) < 4:
            message.message = message.message + "Waiting for " + str(4-len(player)) +" player to play this game\n\n"
        
        conn.send(pickle.dumps(message))
        time.sleep(2)
        start_new_thread(chatThread,(conn,addr))   


        


if __name__ == "__main__": 
    
    getAllPlayers()
    
    setTurn()
    
    Finish = False
    
    broadcast(Message("NOTIFICATION", "Game Begin"))
    playerNow = turn.get()
    turn.put(playerNow)


    while not Finish:
        time.sleep(2)
        broadcast(Message("ONBOARD", cards_on_board))
        time.sleep(2)
        playerNow.send(pickle.dumps(Message("PLAY","play")))

        message = playerNow.recv(2048)
        while not message:
            message = playerNow.recv(2048)
        print message.message
        
        # card = pickle.loads(card)
        # print "onBoard: \n"
        # print "value: " + str(card.number) + "\ttype: " + str(card.type) + "\n\n"
        message = pickle.loads(message)
        print message.type
        if message.type == 'CHAT':
            broadcast(Message('CHAT', message.message))
            print message.message

        # cards_on_board = []
        
        # cards_on_board.append(card)

        # playerNow = turn.get()
        # turn.put(playerNow)


server.close()