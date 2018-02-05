from . import handlers
from .misc import Path

paths = [
    Path(r'^ping$', handlers.PingHandler.as_f()),
    Path(r'^/status$', handlers.StatusHandler.as_f()),
    Path(r'^/activate$', handlers.activate),
    Path(r'^/deactivate$', handlers.deactivate),
    Path(r'^/setlocation( (?P<location>.+))*', handlers.setlocation),
    Path(r'^me$', handlers.me),
    Path(r'.*', handlers.unrecognized),
]
