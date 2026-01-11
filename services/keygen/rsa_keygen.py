from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes


def keygen():
    key = RSA.generate()
    priv_key = key.export_key()
    pub_key = key.public_key().export_key()

    return (pub_key, priv_key)
