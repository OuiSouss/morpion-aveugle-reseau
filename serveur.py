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
    s.listen(2)
    players = []
    players.append(s)

    grids = [grid(),grid(),grid()]
    current_player = J1
        
    while grids[0].gameOver() == -1:
        (s2,addr) = s.accept()
        print("Conection :", addr)
        players.append(s2)
        if len(players) >= 3:
            if current_play
    for p in players:
        p.close()
    s.close()

main()
