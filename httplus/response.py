import json


class Response:
    def __init__(self):
        self.status = 200
        self.message = ''
        self.version = ''
        self.headers = {}
        self.raw = b''
        self.body = b''
        self.content_type = ''
        self.content_length = 0

    def __repr__(self):
        return f'{self.__class__}:{self.status} - {self.content_type.lower()}'

    def set_controller(self, line: bytes):
        self.raw += line
        version, status, message = line.decode().split(' ', maxsplit=2)
        self.status = int(status)
        self.message = message[:-4]
        self.version = version

    def set_header_pair(self, line: bytes):
        self.raw += line
        key, value = line.decode().split(':', maxsplit=1)
        self.headers[key] = value[:-2].strip()
        if key == 'Content-Type':
            self.content_type = value
        elif key == 'Content-Length':
            self.content_length = int(value)

    def set_body(self, line: bytes):
        self.body = line

    def json(self) -> dict | list:
        try:
            res = json.loads(self.body)
            return res
        except Exception as e:
            return None
