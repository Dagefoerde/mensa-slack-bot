import logging
import requests
import datetime
from flufl.enum import Enum

from xml.etree import ElementTree

leo_uri = 'http://speiseplan.stw-muenster.de/mensa_da_vinci.xml'

class FoodIconEnum(Enum):
    fis = ':fish: '
    rin = ':cow: '
    sch = ':pig: '
    gfl = ':chicken: '
    vgt = ':eggplant: '


def getMenues():
    logging.debug('Trying to get Menues from Leo')
    try:
        response = requests.get(leo_uri);
    except requests.exceptions.Timeout as timeOutException:
        logging.error('Could not get Information from STW-Muenster.de: '+timeOutException.message)
        return

    menue = ElementTree.fromstring(response.content)
    print response.content
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

                # Python EAFP concept
                if mealIcon is not None and mealIcon.text is not None:
                    try:
                        mealDescription = FoodIconEnum[str.lower(mealIcon.text)].value + mealDescription
                    except ValueError as valueErr:
                        logging.error('We have no mapping in our FoodIconEnum for the ' + mealIcon.text + ' icon: '
                                      + valueErr.message)

                menueMessage.append(mealDescription)

    return menueMessage