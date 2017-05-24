import logging
import schedule
import slackMensaBot
import threading
import time
import requests
import mensa

infoTime = "11:00"

# Check if we the coffee machine is active, if it is, deactivate it and notify the slack channel. Used by scheduleRunner every day at 8 pm
def mensaInformer():
    # type: () -> dict
    logging.debug('Starting mensaInformer run')
    try:
        slackMensaBot.messageSlackWithMensaMessage(mensa.getMenues())
    except requests.exceptions.Timeout as timeOut:
         logging.error("Cron tried to get Mensa Information. Encountered: " + timeOut.message)


# Clears the queue and sets our shutdown task
def scheduleCleanAndSetup():
    schedule.clear()
    schedule.every().day.at(infoTime).do(mensaInformer)


# http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# This is a Thread that checks our schedule Queue for actionable items
class ScheduleRunner(threading.Thread):
    __metaclass__ = Singleton
    threading.Thread.daemon = True

    @classmethod
    def run(cls):
        while True:
            schedule.run_pending()
            time.sleep(60)
