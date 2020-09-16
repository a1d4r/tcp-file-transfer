import asyncio
from pathlib import Path


FILES_DIR = Path(__file__).parent.absolute() / 'server_files'
FILES_DIR.mkdir(parents=True, exist_ok=True)


class FileWriter:

    def write(self, data):
        filename, data = data.split(b'\n', 1)
        with open(FILES_DIR / filename.decode(), 'wb') as f:
            f.write(data)


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