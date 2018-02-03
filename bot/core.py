#!/usr/bin/env python3
import re
from telepot import Bot as BaseBot
from telepot.loop import MessageLoop
from .settings import TELEGRAM_TOKEN, MIDDLEWARE
from .paths import paths
from .misc import Request


class Dispatcher:
    """Handles the dispatching of incoming Request objects"""

    def __init__(self, paths=None, middleware=None):
        self.paths = paths or []
        self.middleware = middleware or []

    def dispatch(self, request):
        self.apply_middleware(request)
        for path in self.paths:
            match = re.match(path.re_path, request.text)
            if match:
                arguments = match.groupdict()
                return path.handler(request, **arguments)
        raise self.NoFittingPathError()

    def apply_middleware(self, request):
        for middleware in self.middleware:
            middleware(request)

    class NoFittingPathError(Exception):
        """Thrown by `dispatch` method when a Request cannot be dispatched to any of the paths"""
        pass


class Bot(BaseBot):
    def __init__(self):
        super().__init__(TELEGRAM_TOKEN)
        self.dispatcher = Dispatcher(paths, MIDDLEWARE)

    def handle_message(self, meta):
        request = Request(meta)
        try:
            response = self.dispatcher.dispatch(request)
        except Dispatcher.NoFittingPathError:
            #TODO: Handle undispatched request
            return

        if response.text:
            self.sendMessage(request.chat_id, response.text)

    def run(self):
        MessageLoop(self, self.handle_message).run_forever()
