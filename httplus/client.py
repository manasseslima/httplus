import ssl
import asyncio
import socket
from .request import Request
from .response import Response


class Client:
    def __init__(self, verify: str = ''):
        self.verify = verify
        self.writer: asyncio.StreamWriter | None = None
        self.reader: asyncio.StreamReader | None = None

    def __aenter__(self):
        ...

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()

    async def execute(self, host, port, data) -> Response:
        context = None
        if self.verify:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.load_verify_locations(self.verify)
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
        reader, writer = await asyncio.open_connection(host, port, ssl=context)
        writer.write(data)
        await writer.drain()
        response = Response()
        line = await reader.readline()
        response.set_controller(line)
        while True:
            line = await reader.readline()
            if not line or line == b'\r\n':
                break
            response.set_header_pair(line)
        if response.content_length:
            while True:
                line = await reader.read(1000)
                if not line:
                    break
                response.body += line
        writer.close()
        await writer.wait_closed()
        return response

    async def request(
            self,
            method: str,
            url: str,
            data: ... = None,
            headers: dict = None
    ) -> Response:
        headers = headers or {}
        req = Request(url=url, method=method, headers=headers)
        req.set_data(data)
        content = req.render()
        res = await self.execute(req.host, req.port, content)
        return res

    async def get(
            self,
            url: str,
            headers: dict = None
    ) -> Response:
        return await self.request('GET', url, headers=headers)

    async def post(
            self,
            url: str,
            data: ... = None,
            headers: dict = None
    ) -> Response:
        if not data:
            raise Exception(f'Data must be set!')
        return await self.request('POST', url, data, headers)

    async def put(
            self,
            url: str,
            data: ... = None,
            headers: dict = None
    ) -> Response:
        if not data:
            raise Exception(f'Data must be set!')
        return await self.request('PUT', url, data, headers)

    async def delete(
            self,
            url: str,
            data: ... = None,
            headers: dict = None
    ) -> Response:
        return await self.request('DELETE', url, data, headers)

    async def patch(
            self,
            url: str,
            data: ... = None,
            headers: dict = None
    ) -> Response:
        if not data:
            raise Exception(f'Data must be set!')
        return await self.request('PATCH', url, data, headers)

    async def options(
            self,
            url: str,
            data: ... = None,
            headers: dict = None
    ) -> Response:
        return await self.request('OPTIONS', url, data, headers)

    async def header(
            self,
            url: str,
            data: ... = None,
            headers: dict = None
    ) -> Response:
        return await self.request('HEADER', url, data, headers)
