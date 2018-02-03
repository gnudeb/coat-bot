from . import handlers
from .misc import Path

paths = [
    Path(r'^/status$', handlers.status),
    Path(r'^/activate$', handlers.activate),
    Path(r'^/deactivate$', handlers.deactivate),
    Path(r'^me$', handlers.me),
    Path(r'^ping$', handlers.ping),
    Path(r'.*', handlers.unrecognized),
]
