import socket

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(("192.168.200.28",9999)) 

msg='hi'
data=msg.encode("utf-8")

client.sendall(data)