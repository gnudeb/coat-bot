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

def activate(request):
    if not request.user.active:
        request.user.active = True
        request.db.commit()
        response_text = "Bot activated!"
    else:
        response_text = "Bot is already active"

    return Response(response_text)

def deactivate(request):
    if request.user.active:
        request.user.active = False
        request.db.commit()
        response_text = "Bot deactivated!"
    else:
        response_text = "Bot is already deactivated"

    return Response(response_text)