from . import handlers
from .misc import Path

paths = [
    Path(r'^increment (?P<number>[0-9]+)$', handlers.increment),
    Path(r'^ping$', handlers.ping),
    Path(r'.*', handlers.unrecognized),
]
