from collections import namedtuple

Path = namedtuple('Path', ['re_path', 'handler'])

class Handler:
    response_template = ""

    def __init__(self):
        self.context = {}

    @classmethod
    def as_f(cls):
        def handler(request, **kwargs):
            self = cls()
            self.handle(request)
            return Response(cls.response_template.format(**self.context))
        return handler

    def handle(self, request):
        self.context = {}


class Request:
    def __init__(self, meta):
        self.meta = meta
        self.chat_id = meta['from']['id']
        self.text = meta['text']

class Response:
    def __init__(self, text=None):
        self.text = text
