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
    if current_player == J1:
        player1.send(str.encode("turn"))
    else:
        player2.send(str.encode("turn"))
""" Goal put pion where current player wants to put it (shot)
    Modification of the grid in the viewer view
    send of the view corresponding to the current player
    data is the data received after choise of the client
    player is the socket of the current player
"""
def play(data,player, players):
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
        for i in range (3, len(players)):
            players[i].send(str.encode(grids[0].displayStr()))
        current_player = current_player%2 + 1

def main():
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(("",7777))
    print("Serveur pret\n")
    print("Wait connection ...\n")
    s.listen(10)
    players = []
    players.append(s)
    global current_player, grids
    grids = [grid(),grid(),grid()]
    current_player = J1
        
    while grids[0].gameOver() == -1:
        (s2,addr) = s.accept()
        print("Conection :", addr)
        players.append(s2)
        if len(players) >= 3:
            print("il y a assez de joueurs connectés pour lancer le jeu")
            #envoyer les vues a chaque joueur et observateurs
            players[1].send(str.encode(grids[J1].displayStr()))
            players[2].send(str.encode(grids[J2].displayStr()))
            for i in range(3, len(players)):
                players[i].send(str.encode(grids[0].displayStr()))
            for i in range (1,3):
                turn(players[J1],players[J2])
                data_recv_client = players[i].recv(1024)
                if len(data_recv_client) == 0:
                    #we suppose its because one of the player is disconnected
                    #closing the server
                    s.close()
                #turn of player 1
                elif players[i] == players[J1] and current_player == J1:
                    play(data_recv_client,players[i], players)
                #turn of player 2
                elif players[i] == players[J2] and current_player == J2:
                    play(data_recv_client,players[i], players)
                        


    # Game end     
    for p in players:
        p.send(str.encode("GAME OVER!!!"))
        p.send(str.encode(grids[0].displayStr()))
        p.close()
    if grids[0].gameOver() == J1:
        players[J1].send(str.encode("You Win!!!"))
        players[J2].send(str.encode("You Loose!!!"))
        for i in range(3, len(players)):
            players[i].send(str.encode("Player 1 win against player 2 !!!"))
    elif grids[0].gameOver() == J2:
        players[J1].send(str.encode("You Loose!!!"))
        players[J2].send(str.encode("You Win!!!"))
        for i in range(3, len(players)):
            players[i].send(str.encode("Player 2 win against player 1 !!!"))
    else:
        for p in players:
            p.send(str.encode("Draw!!!"))
    s.close()

main()
