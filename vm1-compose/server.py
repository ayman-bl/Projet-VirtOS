import socket 

server=socket.socket(socket.AF_INET , socket.SOCK_STREAM)


server.bind("0.0.0.0",9999)

server.listen()

while True:
    client_socket , address = server.accept()
    client_data= (client_socket.recv(4096)).decode("utf-8")
    client_socket.close()

