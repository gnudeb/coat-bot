from collections import namedtuple

Path = namedtuple('Path', ['re_path', 'handler'])

class Handler:
    response_template = ""

    @classmethod
    def as_f(cls):
        def handler(request, **kwargs):
            context = cls.generate_context(request)
            return Response(cls.response_template.format(**context))
        return handler

    @classmethod
    def generate_context(cls, request):
        return {}


class Request:
    def __init__(self, meta):
        self.meta = meta
        self.chat_id = meta['from']['id']
        self.text = meta['text']

class Response:
    def __init__(self, text=None):
        self.text = text
