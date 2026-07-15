import socket
import threading

commands = [
    b'*1\r\n$4\r\nPING\r\n',
    b'*3\r\n$3\r\nSET\r\n$4\r\nname\r\n$7\r\nDeborah\r\n',
    b'*2\r\n$3\r\nGET\r\n$4\r\nname\r\n',
]

def send_command(client_id, command):
    s = socket.socket()
    s.connect(('127.0.0.1', 6379))
    s.sendall(command)
    response = s.recv(1024)
    print(f"Client {client_id} got: {response}")
    s.close()

threads = []
for i in range(3):
    t = threading.Thread(target=send_command, args=(i+1, commands[i]))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()