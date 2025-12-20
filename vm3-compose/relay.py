import socket


relay_recv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

relay_recv.bind(("0.0.0.0",9999))

relay_recv.listen()

while True:
    relay_send=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_data , addr = relay_recv.accept()
    data=client_data.recv(4096).decode("utf-8")

    if addr[0] =='192.168.200.29':
        relay_send.connect(("192.168.200.28",9999))
        data_encoded=data.encode("utf-8")
        relay_send.sendall(data_encoded)
        client_data.close()
    elif addr[0] == '192.168.200.28':
        relay_send.connect(("192.168.200.29",9999))
        data_encoded=data.encode("utf-8")
        relay_send.sendall(data_encoded)
        client_data.close()

    relay_send.close()


