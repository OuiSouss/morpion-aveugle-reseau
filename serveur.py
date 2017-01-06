#§/usr/bin/env python3

from grid import *
import  random
import sys
import socket


def main():
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(("",7777))
    print("Serveur pret\n")
    print("Wait connection ...\n")
    s.listen(10)
    players = []
    players.append(s)

    grids = [grid(),grid(),grid()]
    current_player = J1
        
    while grids[0].gameOver() == -1:
        (s2,addr) = s.accept()
        print("Conection :", addr)
        players.append(s2)
        if len(players) >= 3:
            print("il y a assez de joueurs connectés pour lancer le jeu")
            #envoyer les vues a chaque joueur
            players[1].send(str.encode(grids[J1].displayStr()))
            players[2].send(str.encode(grids[J2].displayStr()))
            for i in range(3, len(players)):
                players[i].send(str.encode(grids[0].displayStr()))
    for p in players:
        p.close()
    s.close()

main()
