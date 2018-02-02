from collections import namedtuple

Path = namedtuple('Path', ['re_path', 'handler'])

class Response:
    def __init__(self, text=None):
        self.text = text
