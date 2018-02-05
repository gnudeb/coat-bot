from .misc import Response, Handler

class PingHandler(Handler):
    response_template = "pong"


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


def setlocation(request, location):
    if location is not None:
        request.user.location = location
        request.db.commit()
        response_text = "Got it, your location is {}".format(location)
    else:
        response_text = (
            "Use this command as follows: /setlocation <location>\n"
            "Example: /setlocation Kyiv"
        )

    return Response(response_text)
