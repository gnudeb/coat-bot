from . import handlers
from .misc import Path

paths = [
    Path(r'^/status$', handlers.status),
    Path(r'^me$', handlers.me),
    Path(r'^ping$', handlers.ping),
    Path(r'.*', handlers.unrecognized),
]
