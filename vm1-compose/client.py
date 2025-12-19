import socket

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect("192.168.200.32",9999)

client.encode("utf-8").sendall()