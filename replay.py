import socket, sys, json, os
from payloads import *


def replay_attack():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (sys.argv[1], int(sys.argv[2]))
    # s.bind(('127.0.0.1', 8084))

    s.sendto('FAIL', address)
    # s.close()
    while True:
        encrypt_msg, addr = s.recvfrom(65535)
        print encrypt_msg


if __name__ == '__main__':
    # for i in range(1, 1000):
    replay_attack()
