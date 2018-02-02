import os.path
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PRIVATE_FILE_NAME = 'private.json'
PRIVATE_FILE_PATH = os.path.join(BASE_DIR, PRIVATE_FILE_NAME)

with open(PRIVATE_FILE_PATH, 'r') as f:
    data = json.load(f)
    TELEGRAM_TOKEN = data.get('TELEGRAM_TOKEN')


DATABASE_PATH = os.path.join(BASE_DIR, 'tg.db')
DATABASE_URI = 'sqlite:///' + DATABASE_PATH

from . import middleware
MIDDLEWARE = [
    middleware.inject_db_session,
    middleware.autoregister_new_user,
]
