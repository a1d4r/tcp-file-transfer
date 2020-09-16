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
    """Class for writing raw data to a file."""

    def __init__(self):
        self.filename = None
        self.buffer = b''

    def write_buffer(self, data):
        """Buffer the data that has to be written in a file.
        The name of the file and its content is stored in data separated by EOL."""
        if self.filename is None:
            filename, self.buffer = data.split(b'\n', 1)
            self.filename = filename.decode()
        else:
            self.buffer += data

    def fix_filename_collisions(self):
        """Return a filename which won't collide with existing files."""
        # If there is no such file yet the specified filename is ok
        if not (FILES_DIR / self.filename).exists():
            return
        # Split filename into name and extension
        name, ext = os.path.splitext(self.filename)
        new_filename = f'{name}_copy{ext}'
        # Find suitable filename for the copy
        copy_number = 0
        while (FILES_DIR / new_filename).exists():
            copy_number += 1
            new_filename = f'{name}_copy{copy_number}{ext}'
        self.filename = new_filename

    def write(self):
        self.fix_filename_collisions()
        with open(FILES_DIR / self.filename, 'wb') as f:
            f.write(self.buffer)


class FileTransferProtocol(asyncio.Protocol):
    """TCP transfer protocol"""

    def connection_made(self, transport):
        self.filewriter = FileWriter()
        self.transport = transport

    def data_received(self, data):
        self.filewriter.write_buffer(data)

    def connection_lost(self, data):
        self.filewriter.write()
        

async def main(host, port):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(FileTransferProtocol, host, port)
    await server.serve_forever()


asyncio.run(main('', PORT))