import logging
import cron
import requests
from requests.models import Response
logging.basicConfig(filename='mensa.log', level=logging.ERROR)

slackURL = 'https://hooks.slack.com/services/....<insert URL here>'

colors = ["#36a64f","#3AA3E3","warning"]

def messageSlackWithMensaMessage(mensaInformation):
    # type: (dict) -> Response
    if mensaInformation is None and mensaInformation < 1:
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

import mensa
if __name__ == "__main__":
    cron.ScheduleRunner().start()
    cron.scheduleCleanAndSetup()

