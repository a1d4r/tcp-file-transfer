import asyncio
from pathlib import Path
import os


FILES_DIR = Path(__file__).parent.absolute() / 'server_files'
FILES_DIR.mkdir(parents=True, exist_ok=True)


class FileWriter:

    def write(self, data):
        filename, data = data.split(b'\n', 1)
        filename = self.avoid_filename_collisions(filename.decode())
        with open(FILES_DIR / filename, 'wb') as f:
            f.write(data)

    def avoid_filename_collisions(self, filename):
        if not (FILES_DIR / filename).exists():
            return filename
        name, ext = os.path.splitext(filename)
        new_filename = f'{name}_copy{ext}'
        copy_number = 0
        while (FILES_DIR / new_filename).exists():
            copy_number += 1
            new_filename = f'{name}_copy{copy_number}{ext}'
        return new_filename


class FileTransferProtocol(asyncio.Protocol):

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


asyncio.run(main('', 5000))