from .db import Session
from .models import User

def inject_db_session(request):
    request.db = Session()

def autoregister_new_user(request):
    db = Session()
    if not db.query(User).get(request.chat_id):
        user = User(id=request.chat_id)
        db.add(user)
        db.commit()

def inject_user(request):
    request.user = request.db.query(User).get(request.chat_id)
