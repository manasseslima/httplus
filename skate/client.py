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

    async def execute(self, url, data) -> bytes:
        if self.verify:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.load_verify_locations(self.verify)
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
        else:
            context = None
        self.reader, self.writer = await asyncio.open_connection(url, port, ssl=context)
        if data:
            self.writer.write(data.encode())
        data_res = b''
        while True:
            res = await self.reader.read(100)
            if not res:
                break
            data_res += res
        return data_res

    async def request(
            self,
            method: str,
            url: str,
            data: ... = None,
            headers: dict = None
    ) -> Response:
        req = Request(method=method)
        req.url = url
        req.headers = headers or {}
        req.body = data or b''
        res = await self.execute(url, data)
        response = Response(res)
        return response

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
        return await self.request('POST', url, data, headers)

    async def put(
            self,
            url: str,
            data: ... = None,
            headers: dict = None
    ) -> Response:
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