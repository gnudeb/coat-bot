from . import handlers
from .misc import Path

paths = [
    Path(r'^ping$', handlers.ping),
    Path(r'.*', handlers.unrecognized),
]
