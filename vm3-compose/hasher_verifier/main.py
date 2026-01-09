import socket
import json
from verifier import verify_message

HOST = "0.0.0.0"
PORT = 7000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("[VM3] Hasher/Verifier listening on 0.0.0.0:7000")

while True:
    conn, addr = server.accept()
    with conn:
        try:
            data = conn.recv(4096).decode("utf-8")
            if not data:
                conn.sendall(b"not ok")
                continue

            request = json.loads(data)

            valid = verify_message(
                request["data"],
                request["hash"]
            )

            if valid:
                conn.sendall(b"ok")
            else:
                conn.sendall(b"not ok")

        except Exception:
            conn.sendall(b"not ok")
