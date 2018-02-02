import sys
from bot.core import Bot
import bot.models
from bot.db import Base, engine

if len(sys.argv) < 2:
    sys.exit()

argument = sys.argv[1]
#TODO: Ugly!!!
if argument == 'runserver':
    bot = Bot()
    bot.run()
elif argument == 'init_db':
    Base.metadata.create_all(engine)