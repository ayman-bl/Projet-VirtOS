import socket


def sendToVM3(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.200.23", 9999))
    data = data.encode("utf-8")
    client.sendall(data)
    client.close()
