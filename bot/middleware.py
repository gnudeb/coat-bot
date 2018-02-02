from .db import Session

def inject_db_session(request):
    request['db'] = Session()