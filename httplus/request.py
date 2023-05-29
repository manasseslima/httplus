

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
        self.body = ''
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
            self.port = host_port_splt[1]
        else:
            self.port = 433 if self.issecurity else 80
        self.host = f'{"https://" if self.issecurity else "http://"}{host_port_splt[0]}'

    def render(self) -> str:
        headers = '\r\n'.join([f'{k}={v}' for k, v in self.headers.items()])
        content = f'{self.method} {self.uri} {self.version}\r\n{headers}\r\n'
        if self.body:
            content += f'\r\n{self.body}'
        return content
