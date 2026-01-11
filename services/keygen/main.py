import socket
from rsa_keygen import keygen

def sendToVM3(data):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("192.168.200.23",9999))
    data=data.encode("utf-8")
    client.sendall(data)
    client.close()

docker1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

docker1.bind(("0.0.0.0"),7000))

docker1.listen()

while True:
    client_socket , address = docker1.accept()
    client_data= (client_socket.recv(4096)).decode("utf-8")
    client_socket.close()
    encrypted_data=keygen((client_data))
    sendToVM3(encrypted_data)


