import socket
from pathlib import Path
import argparse

# Command line arguments
parser = argparse.ArgumentParser(description="Transfer a file to a server")
parser.add_argument('file', type=str, help='path to the file')
parser.add_argument('server', type=str, help='domain name or ip address of the server')
parser.add_argument('port', type=int, help='port number')

args = parser.parse_args()
HOST = args.server
PORT = args.port
FILEPATH = Path(args.file)


print('Connecting...')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Establish TCP connection with the server
    sock.connect((HOST, PORT))
    print('Connection has been established.')
    # Read file content
    with open(FILEPATH, 'rb') as f:
        data = f.read()
    # Send file name and its content to the socket
    sock.sendall((FILEPATH.name + '\n').encode())
    sock.sendall(data)

print('File has been successfully transfered.')
