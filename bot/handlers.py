from .misc import Response
from .models import User

def ping(request):
    return Response('pong')

def unrecognized(request):
    return Response("Sorry, I don't recognize this command")

def me(request):
    return Response("{0}".format(request.user.id))

def status(request):
    location = request.user.location or "Not set"
    time = request.user.notification_time or "Not set"
    active = request.user.active

    response_text = (
        "Location: {location}\n"
        "Notification time: {time}\n"
        "Bot active: {active}"
    ).format(
        location=location,
        time=time,
        active=active,
    )

    return Response(response_text)
