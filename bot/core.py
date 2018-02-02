#!/usr/bin/env python3
import re
from telepot import Bot as BaseBot
from telepot.loop import MessageLoop
from .settings import TELEGRAM_TOKEN
from .paths import paths


class Bot(BaseBot):
    def __init__(self):
        super().__init__(TELEGRAM_TOKEN)
        self.paths = paths

    def handle_message(self, meta):
        text = meta.get('text')
        chat_id = meta['from']['id']
        for path in self.paths:
            match = re.match(path.re_path, text)
            if match:
                response = path.handler(meta, **match.groupdict())
                if response.text:
                    self.sendMessage(chat_id, response.text)
                return

    def run(self):
        MessageLoop(self, self.handle_message).run_forever()
