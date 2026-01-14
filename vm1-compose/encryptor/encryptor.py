import socket
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 7100))
s.listen(5)

while True:
    connection, address = s.accept()

    raw_data = connection.recv(4096).decode()
    if not raw_data:
        connection.close()
        continue

    data_json = json.loads(raw_data)

    if data_json.get("type") == "START":
        job_id = data_json.get("job_id")
        payload = data_json.get("payload")

        key_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        key_socket.connect(("keygen", 7000))
        key_socket.send(b"PUBKEY\n")

        key_data = key_socket.recv(4096).decode()
        key_json = json.loads(key_data)
        pub_pem = key_json["pubkey"]
        key_socket.close()

        pt = payload.encode()
        random_key = get_random_bytes(32)
        cipher_aes = AES.new(random_key, AES.MODE_GCM)
        ciphertext, auth_tag = cipher_aes.encrypt_and_digest(pt)

        recipient_key = RSA.import_key(pub_pem)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        encrypted_aes_key = cipher_rsa.encrypt(random_key)

        result = {
            "type": "CIPHER",
            "job_id": job_id,
            "dst": "hasher",
            "enc_key": base64.b64encode(encrypted_aes_key).decode(),
            "nonce": base64.b64encode(cipher_aes.nonce).decode(),
            "ct": base64.b64encode(ciphertext).decode(),
            "tag": base64.b64encode(auth_tag).decode(),
        }

        send_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_s.connect(("192.168.200.32", 9999))
        send_s.send(json.dumps(result).encode() + b"\n")
        send_s.close()

    connection.close()
