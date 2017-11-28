#!/usr/bin/env python3

import datetime
from functools import wraps
import logging
from telegram.ext import Updater, CommandHandler
from db import Session, Users
from secret import tg_bot_token

logging.basicConfig(
        level=logging.ERROR,
        format='\t%(asctime)s - %(name)s - %(levelname)s\n%(message)s')

print(datetime.datetime.now())

updater = Updater(tg_bot_token)

def command(pass_args=False):
    def decorator(func):
        @wraps(func)
        def wrapper(bot, update, **args):
            chat_id = update.message.chat_id
            def reply(text):
                bot.send_message(chat_id=chat_id, text=text)
            db_session = Session()
            func(chat_id, reply, db_session, **args)
            db_session.commit()
            db_session.close()

        handler = CommandHandler(
                wrapper.__name__,
                wrapper,
                pass_args=pass_args)

        updater.dispatcher.add_handler(handler)

        return wrapper
    return decorator

@command(pass_args=True)
def test(chat_id, reply, db_session, args):
    reply(str(db_session.query(Users).all()))

def notify_user(bot, job):
    chat_id = job.context["chat_id"]
    bot.send_message(
            chat_id=chat_id,
            text="A notification!")

local_session = Session()
active_users = local_session.query(Users).filter_by(active=True).all()

for user in active_users:
    
    print("Scheduling a notification for user {} at {}".format(user.id, user.time))

    hour, minute = map(int, user.time.split(":"))
    time = datetime.time(hour, minute)

    updater.job_queue.run_daily(
            callback=notify_user,
            time=time,
            context={"chat_id": user.id},
            name=str(user.id))

local_session.close()


def start(bot, update):
    session = Session()
    print("start")
    chat_id = update.message.chat_id
    bot.send_message(
            chat_id=chat_id,
            text="Hi, I am weather tracking bot!")
    if not session.query(Users).filter_by(id=chat_id).first():
        user = Users(id=chat_id)
        session.add(user)
        session.commit()
        bot.send_message(
                chat_id=chat_id,
                text="You are all set! You can check /status now")

    session.close()

start_handler = CommandHandler("start", start)
updater.dispatcher.add_handler(start_handler)

def status(bot, update):
    session = Session()
    print("status")
    chat_id = update.message.chat_id
    user = session.query(Users).filter_by(id=chat_id).first()
    text = "{} {} {} {}".format(
            user.id,
            user.city,
            user.time,
            user.active)

    bot.send_message(
            chat_id=chat_id,
            text=text)

    session.close()

status_handler = CommandHandler("status", status)
updater.dispatcher.add_handler(status_handler)

def set_city(bot, update, args):
    session = Session()
    
    chat_id = update.message.chat_id
    user = session.query(Users).filter_by(id=chat_id).first()
    user.city = args[0]
    session.commit()
    status(bot, update)

    session.close()

set_city_handler = CommandHandler("set_city", set_city, pass_args=True)
updater.dispatcher.add_handler(set_city_handler)

def set_time(bot, update, args):
    session = Session()
    
    chat_id = update.message.chat_id
    user = session.query(Users).filter_by(id=chat_id).first()
    user.time = args[0]
    session.commit()
    status(bot, update)
    # updating a user dedicated job
    print("Updating a job for user {}".format(user.id))
    jobs = updater.job_queue.jobs()
    job_name = str(user.id)
    user_job = next(filter(lambda j: j.name==job_name and j.enabled, jobs))
    user_job.schedule_removal()
    print("Jobs after removal: {}".format(updater.job_queue.jobs()))

    hour, second = map(int, args[0].split(":"))
    new_time = datetime.time(hour, second)

    updater.job_queue.run_daily(
            callback=user_job.callback,
            time=new_time,
            context=user_job.context,
            name=user_job.name)

    session.close()

set_time_handler = CommandHandler("set_time", set_time, pass_args=True)
updater.dispatcher.add_handler(set_time_handler)

def suspend(bot, update):
    session = Session()
    
    chat_id = update.message.chat_id
    user = session.query(Users).filter_by(id=chat_id).first()
    user.active = False
    session.commit()
    status(bot, update)

    session.close()

suspend_handler = CommandHandler("suspend", suspend)
updater.dispatcher.add_handler(suspend_handler)

def restart(bot, update):
    session = Session()
    
    chat_id = update.message.chat_id
    user = session.query(Users).filter_by(id=chat_id).first()
    user.active = True
    session.commit()
    status(bot, update)

    session.close()

restart_handler = CommandHandler("restart", restart)
updater.dispatcher.add_handler(restart_handler)

updater.start_polling()
