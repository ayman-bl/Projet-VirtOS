import socket, json
from Crypto.PublicKey import RSA

HOST = "0.0.0.0"
PORT = 7000

key = RSA.generate(2048)
PUB = key.publickey().export_key().decode()


def send_json(conn, obj):
    conn.sendall((json.dumps(obj) + "\n").encode())


def recv_line(conn):
    data = b""
    while b"\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    return data.split(b"\n", 1)[0].decode().strip()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(20)
print(f"[keygen] listening {HOST}:{PORT}")

while True:
    conn, addr = s.accept()
    try:
        req = recv_line(conn)
        send_json(conn, {"type": "PUBKEY", "pubkey": PUB})
    finally:
        conn.close()
