from .misc import Response
from .models import User

def ping(request):
    return Response('pong')

def unrecognized(request):
    return Response("Sorry, I don't recognize this command")

def me(request):
    return Response("{0}".format(request['user'].id))
