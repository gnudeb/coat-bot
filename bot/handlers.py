from .misc import Response
from .models import User

def ping(request):
    print(request['db'].query(User).first())
    return Response('pong')

def unrecognized(request):
    return Response("Sorry, I don't recognize this command")

def increment(request, number):
    number = int(number)
    return Response("{0}".format(number + 1))
