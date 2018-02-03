#!/usr/bin/env python3
import re
from telepot import Bot as BaseBot
from telepot.loop import MessageLoop
from .settings import TELEGRAM_TOKEN, MIDDLEWARE
from .paths import paths
from .misc import Request

class Bot(BaseBot):
    def __init__(self):
        super().__init__(TELEGRAM_TOKEN)
        self.paths = paths
        self.middleware = MIDDLEWARE

    def handle_message(self, meta):
        text = meta.get('text')
        chat_id = meta['from']['id']
        for path in self.paths:
            match = re.match(path.re_path, text)
            if match:
                request = Request(meta)
                self.apply_middleware(request)
                response = path.handler(request, **match.groupdict())
                if response.text:
                    self.sendMessage(chat_id, response.text)
                return

    def apply_middleware(self, request):
        for middleware in self.middleware:
            middleware(request)

    def run(self):
        MessageLoop(self, self.handle_message).run_forever()
