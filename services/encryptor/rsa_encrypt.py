from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def encrypt(msg, pub_key):
    msg = msg.encode("utf-8")
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(pub_key))
    cipher_msg = cipher_rsa.encrypt(msg)

    return cipher_msg
