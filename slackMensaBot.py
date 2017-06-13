import logging
import cron
import requests
import time
from requests.models import Response
import click
from daemonocle.cli import DaemonCLI
logging.basicConfig(filename='mensa.log', level=logging.INFO)

slackURL = 'https://hooks.slack.com/services/....<insert URL here>'

colors = ["#36a64f","#3AA3E3","warning"]

def messageSlackWithMensaMessage(mensaInformation):
    # type: (dict) -> Response
    if mensaInformation is None or len(mensaInformation) < 1:
        return
    logging.debug('Trying to send a message to Slack')

    colorit = iter(colors) # Color Iterator

    payload = {"attachments": []} # initial payload
    for mensaInfoAtom in mensaInformation: #
        payload['attachments'].append(
            {
                "color": 'error' if mensaInfoAtom == 'Geschlossen' else colorit.next(),
                "mrkdwn_in": ["text", "pretext"],
                "text" : mensaInfoAtom
            }
        )
    payload['attachments'][0]["pretext"] = "Lunch Menu for Today :yum:" # Add pretext to first elem

    try:
        return requests.post(slackURL, json=payload, timeout=60)
    except requests.exceptions.Timeout as timeOut:
        logging.error('Could not send a message to Slack: '+timeOut.message)

@click.command(cls=DaemonCLI, daemon_params={'pidfile': 'slackMensaBot.pid'})
def main():
    """This is our Mensa Slack Bot. It will send a daily summary of the Mensa menue to our Slack channel"""
    cron.ScheduleRunner().start()
    cron.scheduleCleanAndSetup()
    while True:
        time.sleep(30)

if __name__ == "__main__":
    main()