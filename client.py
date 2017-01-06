#!/usr/bin/env python3

from grid import *
import  random
import sys
import socket

""" Return an int the reponse of the question
    shot need to be between 0 and 8
"""
def selectCase():
    shot = -1
    while shot<0 or shot>=NB_CELLS:
        shot = int(input("Quelle case allez vous jouer ? (un nombre obligatoirement entre 0 et 8)"))
    return shot

def main(host):
    print("je suis un client")
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.connect((host,7777))
    while True:
        data = str(bytes.decode(s.recv(1024)))
        shot = -1
        if data == "turn":
            shot = selectCase()
            s.send(str.encode(str(shot)))
            data = None
        elif len(data) != 0:
            print(data)



if __name__ == "__main__":
    try:
        host = sys.argv[1]
    except IndexError:
        print ("probleme d'argument sans argument c'est le serveur à lancer")
        sys.exit(1)
    main(host)

