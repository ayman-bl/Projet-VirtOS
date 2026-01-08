from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes


def keygen():
    key = RSA.generate()
    priv_key = key.export_key()
    pub_key = key.public_key().export_key()

    cipher_rsa_pub = PKCS1_OAEP.new(RSA.import_key(pub_key))
    cipher_rsa_prv = PKCS1_OAEP.new(RSA.import_key(priv_key))

    return (pub_key, priv_key)
