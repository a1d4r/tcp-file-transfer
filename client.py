import socket
from pathlib import Path
from tqdm import tqdm
import os
import argparse
import time

# Command line arguments
parser = argparse.ArgumentParser(description="Transfer a file to a server")
parser.add_argument('file', type=str, help='path to the file')
parser.add_argument('server', type=str, help='domain name or ip address of the server')
parser.add_argument('port', type=int, help='port number')

args = parser.parse_args()
HOST = args.server
PORT = args.port
FILEPATH = Path(args.file)

CHUNK_SIZE = 1024

def read_by_chunks(file_object, chunk_size=1024):
    """Read file by chunks"""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        # time.sleep(0.001)
        yield data

total_size = os.path.getsize(FILEPATH)

print('Connecting...')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Establish TCP connection with the server
    sock.connect((HOST, PORT))
    print('Connection has been established.')
    # Read file content
    with open(FILEPATH, 'rb') as f:
        print('Uploading the file...')
        # Send file name and its content to the socket
        sock.sendall((FILEPATH.name + '\n').encode())
        for data in tqdm(iterable=read_by_chunks(f, chunk_size=CHUNK_SIZE), 
                         total=total_size // CHUNK_SIZE, 
                         unit='KB',
                         desc=FILEPATH.name):
             sock.send(data)

print('File has been successfully transfered.')
