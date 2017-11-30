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

def update_jobs_state(job_queue, user):
    jobs = job_queue.jobs()
    job_name = str(user.id)
    user_job = next(filter(lambda j: j.name==job_name and j.enabled==True, jobs), None)
    
    if user_job:
        user_job.schedule_removal()
    
    if user.active:
        hour, second = map(int, user.time.split(":"))
        time = datetime.time(hour, second)
        job_queue.run_daily(
                callback=notify_user,
                time=time,
                context={"chat_id": user.id},
                name=job_name)

def command(pass_args=False):
    def decorator(func):
        @wraps(func)
        def wrapper(bot, update, **args):
            chat_id = update.message.chat_id
            def reply(text):
                bot.send_message(chat_id=chat_id, text=text)
            db_session = Session()
            user = db_session.query(Users).filter_by(id=chat_id).first()
            context = {
                    "user": user,
                    "chat_id": chat_id,
                    "db_session": db_session,
                    "reply": reply}
            func(**context, **args)
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
def start(user, chat_id, db_session, reply):
    reply("Hi, I am weather tracking bot!")
    if not user:
        print("not user")
        user = Users(id=chat_id)
        db_session.add(user)
        reply("You are all set! You can check /status now")


@command()
def status(user, chat_id, db_session, reply):
    text = "{} {} {} {}".format(
            user.id,
            user.city,
            user.time,
            user.active)

    reply(text)


@command(pass_args=True)
def set_city(user, chat_id, db_session, reply, args):
    user.city = args[0]

@command(pass_args=True)
def set_time(user, chat_id, db_session, reply, args):
    user.time = args[0]
    update_jobs_state(updater.job_queue, user)

@command()
def suspend(user, chat_id, db_session, reply):
    user.active = False
    update_jobs_state(updater.job_queue, user)


@command()
def restart(user, chat_id, db_session, reply):
    user.active = True
    update_jobs_state(updater.job_queue, user)

@command()
def help(user, chat_id, db_session, reply):
    reply(
            "/start\n"
            "/status\n"
            "/set_city <city>\n"
            "/set_time <hh:mm>\n"
            "/suspend\n"
            "/restart")



updater.start_polling()
