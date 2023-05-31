import asyncio
import json


lines = [
    'http/1.1 200 OK',
    'Content-Type:application/json',
    'Content-Length:44',
    '',
]


router = {
    '/api/girls': {
        'GET': [
            {
                "id": 1,
                "first_name": "Ino",
                "last_name": "Yamanaka"
            },
            {
                "id": 2,
                "first_name": "Kurenai",
                "last_name": "Yūhi"
            },
            {
                "id": 3,
                "first_name": "Kushina",
                "last_name": "Uzumaki"
            },
            {
                "id": 4,
                "first_name": "Sakura",
                "last_name": "Haruno"
            },
            {
                "id": 5,
                "first_name": "Hinata",
                "last_name": "Hyūga"
            },
            {
                "id": 6,
                "first_name": "Rin",
                "last_name": "Nohara"
            }
        ],
        'POST': {
            "id": 7,
            "first_name": "Karin",
            "last_name": "Uzumaki"
        }
    },
    '/api/girls/1': {
        'GET': {
            "id": 1,
            "first_name": "Ino",
            "last_name": "Yamanaka"
        }
    }
}


class LineGenerator:
    def __init__(self):
        self.pointer = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = f'{lines[self.pointer]}\r\n'.encode()
        self.pointer += 1
        return line


class MockReaderStream:
    def __init__(self, conn):
        self.conn = conn
        self.body = b''
        self.line_generator = LineGenerator()
        self.already_read = False

    async def readline(self):
        return await self.line_generator.__anext__()

    async def read(self, size):
        if self.already_read:
            return b''
        self.already_read = True
        await asyncio.sleep(0.0001)
        body = json.dumps(self.body)
        return body.encode()


class MockWriterStream:
    def __init__(self, conn):
        self.conn = conn

    def write(self, data):
        data_context = data.decode()
        line, data_context = data_context.split('\r\n', maxsplit=1)
        method, uri, version = line.split(' ')
        data = router[uri][method]
        self.conn.reader.body = data

    async def drain(self):
        await asyncio.sleep(0.0002)

    def close(self):
        ...

    async def wait_closed(self):
        await asyncio.sleep(0.0002)


class MockConnection:
    def __init__(self):
        self.reader = None
        self.writer = None

    def generate_streams(self, ):
        reader = MockReaderStream(conn=self)
        writer = MockWriterStream(conn=self)
        self.reader = reader
        self.writer = writer
        return reader, writer


async def mock_connection(host, port, ssl):
    conn = MockConnection()
    return conn.generate_streams()
