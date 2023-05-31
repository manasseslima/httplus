import json


class Request:
    def __init__(
            self,
            url: str,
            method: str = 'GET',
            headers: dict = None
    ):
        self.url = url
        self.host = ''
        self.port = 80
        self.uri = ''
        self.headers = headers or {}
        self.method = method
        self.version = 'http/1.1'
        self.body: bytes = b''
        self.issecurity = True
        self.prepare_host()

    def prepare_host(self):
        if self.url.startswith('http://'):
            self.issecurity = False
            size = 7
        else:
            size = 8
        splt = self.url[size:].split('/', maxsplit=1)
        self.uri = f'/{splt[1]}' if len(splt) > 1 else '/'
        host_port_splt = splt[0].split(':')
        if len(host_port_splt) > 1:
            self.port = int(host_port_splt[1])
        else:
            self.port = 433 if self.issecurity else 80
        self.host = host_port_splt[0]

    def render(self) -> bytes:
        headers = '\r\n'.join([f'{k}:{v}' for k, v in self.headers.items()])
        content = f'{self.method} {self.uri} {self.version}\r\n{headers}\r\n'
        content = content.encode()
        if self.body:
            content += b'\r\n' + self.body
        return content

    def set_data(self, data: ... = None):
        if not data:
            self.body = b''
            return
        if content_type := self.headers.get('Content-Type', ''):
            match content_type:
                case 'application/json':
                    body = json.dumps(data)
                    self.body = body.encode()
                case _:
                    self.body = data
        else:
            body = json.dumps(data)
            self.body = body.encode()
            self.headers['Content-Type'] = 'application/json'
            self.headers['Content-Length'] = len(self.body)
