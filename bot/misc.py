from collections import namedtuple

Path = namedtuple('Path', ['re_path', 'handler'])

class Request:
    def __init__(self, meta):
        self.meta = meta
        self.chat_id = meta['from']['id']
        self.text = meta['text']

class Response:
    def __init__(self, text=None):
        self.text = text
