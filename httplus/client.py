import ssl
import asyncio
import socket
from typing import Optional
from .request import Request
from .response import Response


class Client:
    def __init__(self, verify: str = ''):
        self.verify = verify
        self.writer: asyncio.StreamWriter | None = None
        self.reader: asyncio.StreamReader | None = None
        self.eof = b'\r\n0\r\n\r\n'
        self.empty_line = b'\r\n'
        self.chunk_size = 1000

    def __aenter__(self):
        ...

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()

    async def execute(self, host: str, port: int, data: bytes, security=False) -> Response:
        self.reader, self.writer = await asyncio.open_connection(host, port, ssl=security)
        response = Response()
        try:
            self.writer.write(data)
            await self.writer.drain()
            line = await self.reader.readline()
            response.set_controller(line)
            while True:
                line = await self.reader.readline()
                if not line or line == self.empty_line:
                    break
                response.set_header_pair(line)
            if response.content_length:
                length = response.content_length
                while length:
                    chunk = await self.reader.read(self.chunk_size)
                    response.raw += chunk
                    if not chunk:
                        break
                    response.body += chunk
                    length -= len(chunk)
            else:
                length = 0
                while True:
                    chunk = await self.reader.read(self.chunk_size)
                    response.raw += chunk
                    response.body += chunk
                    length += len(chunk)
                    if chunk.endswith(self.eof):
                        response.body = response.body[6:-7]
                        break
                response.content_length = length
        except Exception as e:
            response.status = 500
            response.message = str(e)
        finally:
            self.writer.close()
            await self.writer.wait_closed()
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
        res = await self.execute(host=req.host, port=req.port, data=content, security=req.issecurity)
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
