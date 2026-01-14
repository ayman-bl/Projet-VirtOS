import socket
import json
import uuid

payload_text = "hello"
job_id = str(uuid.uuid4())[:8]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.200.32", 9999))

msg = {"type": "START", "job_id": job_id, "payload": payload_text, "dst": "encryptor"}

s.send((json.dumps(msg) + "\n").encode())
s.close()
print("Sent the job: " + job_id)

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind(("0.0.0.0", 7300))
srv.listen(5)
print("Waiting for results on port 7300...")

while True:
    conn, addr = srv.accept()

    data = conn.recv(4096).decode()
    if data:
        result_json = json.loads(data)
        print("Got a result back!")
        print(result_json)

    conn.close()
