import logging
import requests
import datetime
from enum import Enum

from xml.etree import ElementTree

leo_uri = 'http://speiseplan.stw-muenster.de/mensa_da_vinci.xml'

class FoodIconEnum(Enum):
     Rin = ':cow:'
     Sch = ':pig:'
     Gfl = ':chicken:'
     Vgt = ':eggplant:'


def getMenues():
    logging.debug('Trying to get Menues from Leo')
    try:
        response = requests.get(leo_uri);
    except requests.exceptions.Timeout as timeOutException:
        logging.error('Could not get Information from STW-Muenster.de: '+timeOutException.message)
        return

    menue = ElementTree.fromstring(response.content)

    menueMessage = []

    for menuePerDate in menue:
        unixtimestamp = float(menuePerDate.attrib.get('timestamp'))
        lunchDate = datetime.datetime.fromtimestamp(unixtimestamp).date()
        if lunchDate == datetime.datetime.now().date():
            dishes = list(menuePerDate.iter('item'))
            for dish in dishes:
                meal = dish.find('meal').text
                mealIcon = dish.find('foodicons')

                mealDescription = meal + '*Tagesaktion*' if dish.find('category').text == 'Tagesaktion' else meal

                if mealIcon is not None or FoodIconEnum[mealIcon.text] is not None:
                    mealDescription = FoodIconEnum[mealIcon.text].value + ' ' + mealDescription

                menueMessage.append(mealDescription)

    return menueMessage