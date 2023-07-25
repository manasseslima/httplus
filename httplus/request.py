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
        self.method = method
        self.version = 'HTTP/1.1'
        self.body: bytes = b''
        self.issecurity = True
        self.prepare_host()
        self.headers = self.generate_headers(headers or {})

    def prepare_host(self):
        if self.url.startswith('http://'):
            self.issecurity = False
            size = 7
        elif self.url.startswith('www'):
            size = 0
        else:
            size = 8
        splt = self.url[size:].split('/', maxsplit=1)
        self.uri = f'/{splt[1]}' if len(splt) > 1 else '/'
        host_port_splt = splt[0].split(':')
        if len(host_port_splt) > 1:
            self.port = int(host_port_splt[1])
        else:
            self.port = 443 if self.issecurity else 80
        self.host = host_port_splt[0]

    def render(self) -> bytes:
        headers = '\r\n'.join([f'{k}:{v}' for k, v in self.headers.items()])
        content = f'{self.method} {self.uri} {self.version}\r\n{headers}\r\n'
        content = content.encode()
        content += b'\r\n'
        if self.body:
            content += self.body
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

    def generate_headers(self, headers: dict):
        n_headers = {
            'Host': self.host,
            'User-Agent': 'httplus/0.1.1',
            'Accept': '*/*'
        }
        n_headers.update(headers)
        return n_headers
