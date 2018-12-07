import os,base64,sys, random, binascii, datetime
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding as paddingdatalib

"""
Team venkatesan-saisujitha's encryption methods
"""
# RSA Encryption of the Key
def RSAencryption(keytypes, message):
    ciphertext = keytypes.encrypt(message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA512()), algorithm=hashes.SHA256(), label=None))
    return ciphertext


# RSA Decryption of the Key
def RSAdecryption(keytypes, ciphertext):
    plaintext = keytypes.decrypt(ciphertext, padding.OAEP(mgf = padding.MGF1(algorithm=hashes.SHA512()), algorithm = hashes.SHA256(), label = None))
    return plaintext


# read the public key from file
def readRSApublicKey(publickeyfilename):
    with open(publickeyfilename, "rb") as public_key_file:
        publickey = serialization.load_der_public_key(public_key_file.read(), backend=default_backend())
    return publickey


# read the private key from file
def readRSAprivateKey(privatekeyfilename):
    with open(privatekeyfilename, "rb") as private_key_file:
        privatekey = serialization.load_der_private_key(private_key_file.read(), password = None, backend = default_backend())
    return privatekey

# read the private key from file
def readRSApemPrivateKey(privatekeyfilename):
    with open(privatekeyfilename, "rb") as private_key_file:
        privatekey = serialization.load_pem_private_key(private_key_file.read(), password = None, backend = default_backend())
    return privatekey




# Encrypting Public Key
def keyEncryption(key, message):
    parts=[message[i:i + 48] for i in range(0, len(message), 48)]
    i=0
    encrypted=[]
    for i in range(0,len(parts)):
        encrypted.append(RSAencryption(key , parts[i]))
    return encrypted
