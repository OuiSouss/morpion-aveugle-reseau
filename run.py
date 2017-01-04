#!/usr/bin/python3

import socket

def select_mode(host):
    """ select server or client mode
    host integer to specify which mode to select
    """
    if host == "":
        run_server()
    else:
        run_client(host)

def run_server():
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(("",7777))
    s.listen(2)
    print("Wait connection ...")
    players = []
    
    while True:
        (s2,addr) = s.accept()
        print("Conection :", addr)

def run_client(host):
    
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.connect((host,7777))
