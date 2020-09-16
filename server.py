import asyncio
from pathlib import Path
import argparse
import os

# Directory for storing uploaded files
FILES_DIR = Path(__file__).parent.absolute() / 'server_files'
# Create directory if it's not exist
FILES_DIR.mkdir(parents=True, exist_ok=True)

PORT = 5000

class FileWriter:
    """Class for writing raw data to files."""
    def write(self, data):
        """Write binary data to a file. 
        The name of the file and its content is stored in data separated by EOL."""
        filename, data = data.split(b'\n', 1)
        filename = self.avoid_filename_collisions(filename.decode())
        with open(FILES_DIR / filename, 'wb') as f:
            f.write(data)

    def avoid_filename_collisions(self, filename):
        """Return a filename which won't collide with existing files."""
        # If there is no such file yet the specified filename is ok
        if not (FILES_DIR / filename).exists():
            return filename
        # Split filename into name and extension
        name, ext = os.path.splitext(filename)
        new_filename = f'{name}_copy{ext}'
        # Find suitable filename for the copy
        copy_number = 0
        while (FILES_DIR / new_filename).exists():
            copy_number += 1
            new_filename = f'{name}_copy{copy_number}{ext}'
        return new_filename


class FileTransferProtocol(asyncio.Protocol):
    """TCP transfer protocol"""
    def __init__(self):
        self.filewriter = FileWriter()
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.filewriter.write(data)
        

async def main(host, port):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(FileTransferProtocol, host, port)
    await server.serve_forever()


asyncio.run(main('', PORT))