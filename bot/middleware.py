from .db import Session
from .models import User

def inject_db_session(request):
    request['db'] = Session()

def autoregister_new_user(request):
    chat_id = request['from']['id']
    db = Session()
    if not db.query(User).get(chat_id):
        user = User(id=chat_id)
        db.add(user)
        db.commit()

def inject_user(request):
    chat_id = request['from']['id']
    db = Session()
    user = db.query(User).get(chat_id)
    db.expunge(user)
    request['db'].add(user)
    request['user'] = user
