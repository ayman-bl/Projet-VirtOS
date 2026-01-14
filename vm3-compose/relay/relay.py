import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 9999))
s.listen(10)

print("Relay server is running...")

while True:
    connection, address = s.accept()

    data = b""
    while b"\n" not in data:
        chunk = connection.recv(4096)
        if not chunk:
            break
        data += chunk

    data = data.split(b"\n", 1)[0].decode().strip()
    if not data:
        connection.close()
        continue

    msg = json.loads(data)
    dst = msg.get("dst")

    if dst == "encryptor":
        out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_socket.connect(("192.168.200.28", 7100))
        out_socket.sendall((json.dumps(msg) + "\n").encode())
        out_socket.close()
        print("Sent to encryptor")

    elif dst == "hasher":
        out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_socket.connect(("hasher", 7000))
        out_socket.sendall((json.dumps(msg) + "\n").encode())
        out_socket.close()
        print("Sent to hasher")

    elif dst == "windows":
        out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_socket.connect(("192.168.200.29", 7300))
        out_socket.sendall((json.dumps(msg) + "\n").encode())
        out_socket.close()
        print("Sent to windows")

    else:
        print("Error: Unknown destination")

    connection.close()
