import socket 

vm1_server=socket.socket(socket.AF_INET , socket.SOCK_STREAM)


vm1_server.bind("0.0.0.0",9999)

vm1_server.listen()

    