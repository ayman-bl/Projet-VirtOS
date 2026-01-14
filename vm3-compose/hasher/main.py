import socket
import json
import hashlib
import base64

HOST = "0.0.0.0"
PORT = 7000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print("[VM3] Hasher/Verifier listening on 0.0.0.0:7000")

while True:
    conn, addr = server.accept()
    with conn:
        try:
            data = b""
            while b"\n" not in data:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk

            data = data.split(b"\n", 1)[0].decode().strip()
            if not data:
                continue

            request = json.loads(data)

            raw = (
                base64.b64decode(request["enc_key"])
                + base64.b64decode(request["nonce"])
                + base64.b64decode(request["ct"])
                + base64.b64decode(request["tag"])
            )
            h = hashlib.sha256(raw).hexdigest()

            result = {
                "type": "RESULT",
                "job_id": request.get("job_id"),
                "hash": h,
                "ok": True,
                "dst": "windows",
            }

            out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            out_socket.connect(("relay", 9999))
            out_socket.sendall((json.dumps(result) + "\n").encode())
            out_socket.close()

            conn.sendall(b"ok")

        except Exception:
            conn.sendall(b"not ok")
