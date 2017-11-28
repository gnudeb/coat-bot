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

@command()
def start(chat_id, reply, db_session):
    reply("Hi, I am weather tracking bot!")
    if not db_session.query(Users).filter_by(id=chat_id).first():
        user = Users(id=chat_id)
        db_session.add(user)
        reply("You are all set! You can check /status now")


@command()
def status(chat_id, reply, db_session):
    user = db_session.query(Users).filter_by(id=chat_id).first()
    text = "{} {} {} {}".format(
            user.id,
            user.city,
            user.time,
            user.active)

    reply(text)


@command(pass_args=True)
def set_city(chat_id, reply, db_session, args):
    user = db_session.query(Users).filter_by(id=chat_id).first()
    user.city = args[0]

@command(pass_args=True)
def set_time(chat_id, reply, db_session, args):
    user = db_session.query(Users).filter_by(id=chat_id).first()
    user.time = args[0]
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


@command()
def suspend(chat_id, reply, db_session):
    user = db_session.query(Users).filter_by(id=chat_id).first()
    user.active = False


@command()
def restart(chat_id, reply, db_session):
    user = db_session.query(Users).filter_by(id=chat_id).first()
    user.active = True



updater.start_polling()
