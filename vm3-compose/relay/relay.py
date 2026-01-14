import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 9999))
s.listen(10)

print("Relay server is running...")

while True:
    connection, address = s.accept()

    # Simple recv without a loop - classic student approach
    data = connection.recv(4096).decode()
    if not data:
        connection.close()
        continue

    msg = json.loads(data)
    dst = msg.get("dst")

    # Creating a new socket for every single forward inside the if-statements
    if dst == "encryptor":
        out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_socket.connect(("192.168.200.28", 7100))
        out_socket.send((json.dumps(msg) + "\n").encode())
        out_socket.close()
        print("Sent to encryptor")

    elif dst == "hasher_verifier":
        out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_socket.connect(("hasher_verifier", 7200))
        out_socket.send((json.dumps(msg) + "\n").encode())
        out_socket.close()
        print("Sent to hasher_verifier")

    elif dst == "windows":
        out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_socket.connect(("192.168.200.29", 7300))
        out_socket.send((json.dumps(msg) + "\n").encode())
        out_socket.close()
        print("Sent to windows")

    else:
        print("Error: Unknown destination")

    connection.close()
