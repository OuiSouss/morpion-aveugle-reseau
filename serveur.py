#§/usr/bin/env python3

from grid import *
import  random
import sys
import socket

""" Send message to the current player of the game
    we send turn because is the magic word to know that now the client
    can choose the place where he want to put the pion
"""
def turn(player1,player2):
    global current_player
    if player1==None or player2==None:
        return
    elif current_player == J1:
        player1.send(str.encode("turn"))
    else:
        player2.send(str.encode("turn"))
""" Goal put pion where current player wants to put it (shot)
    Modification of the grid in the viewer view
    send of the view corresponding to the current player
    data is the data received after choise of the client
    player is the socket of the current player
"""
def play(data,player):
    global current_player, grids
    shot = int(bytes.decode(data))
    #case not free
    if grids[0].cells[shot] != EMPTY:
        #new print of the grid
        grids[current_player].cells[shot] = grids[0].cells[shot]
        player.send(str.encode(grids[current_player].displayStr()))
    #case free
    else:
        #play shot, new print of the grid
        grids[current_player].cells[shot] = current_player
        grids[0].play(current_player,shot)
        player.send(str.encode(grids[current_player].displayStr()))
        current_player = current_player%2 + 1
    print("au tour de " + str(current_player))

def main():
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(("",7777))
    print("Serveur pret\n")
    print("Wait connection ...\n")
    s.listen(2)
    players = []
    players.append(s)
    global current_player, grids
    grids = [grid(),grid(),grid()]
    current_player = J1
    s_player1 = None
    s_player2 = None
    while grids[0].gameOver() == -1:
        for p in players:
            if p == s :
                if s_player1 == None or s_player2 == None:
                    print("il manque des joueurs")
                    (s2,addr) = s.accept()
                    if s_player1 == None:
                        print("Conection :", addr)
                        s_player1 = s2
                        players.append(s_player1)                        
                        s_player1.send(str.encode(grids[J1].displayStr()))
                    else:
                        print("Connection: ", addr)
                        s_player2 = s2
                        players.append(s_player2)
                        s_player2.send(str.encode(grids[J2].displayStr()))
                        print("on peut commencer")
                        turn(s_player1,s_player2)
                else:
                        s2.send(str.encode("pas de joueur ou d'observateur en plus accepter"))
            else:
                if s_player1 != None and s_player2 != None:
                    data_recv_client = p.recv(1024)
                    if len(data_recv_client) == 0:
                        #we suppose its because one of the player is disconnected
                        #closing the server
                        s.close()
                    #turn of player 1
                    elif p == s_player1 and current_player == J1:
                        play(data_recv_client,p)
                    #turn of player 2
                    elif p == s_player2 and current_player == J2:
                        play(data_recv_client,p)
                    turn(s_player1,s_player2)
                            


    # Game end     
    if grids[0].gameOver() == J1:
        s_player1.send(str.encode("You Win!!!"))
        s_player2.send(str.encode("You Loose!!!"))
    elif grids[0].gameOver() == J2:
        s_player1.send(str.encode("You Loose!!!"))
        s_player2.send(str.encode("You Win!!!"))
    else:
        for p in players:
            p.send(str.encode("Draw!!!"))
    s_player1.close()
    s_player2.close()
    s.close()
if __name__ == "__main__":
    main()
