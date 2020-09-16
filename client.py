import socket
from pathlib import Path

HOST = '127.0.0.1'
PORT = 5000
FILEPATH = Path('./file.txt')


print('Connecting...')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    print('Connection has been established.')
    with open(FILEPATH, 'rb') as f:
        data = f.read()

    sock.sendall((FILEPATH.name + '\n\n').encode())
    sock.sendall(data)
