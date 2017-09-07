import logging
import traceback
import requests
import datetime
from xml.etree import ElementTree

leo_uri = 'http://speiseplan.stw-muenster.de/mensa_da_vinci.xml'
ring_uri = 'http://speiseplan.stw-muenster.de/mensa_am_ring.xml'

mensa_uri = leo_uri

foodIcons = {}
foodIcons['fis'] = ':fish: '
for key in ['rin', 'rnd']:
    foodIcons[key] = ':cow: '
foodIcons['sch'] = ':pig: '
foodIcons['gfl'] = ':chicken: '
foodIcons['vgt'] = ':egg: '
foodIcons['vgn'] = ':seedling: '
foodIcons['alk'] = ':wine_glass: '

def getMenues():
    logging.debug('Trying to get Menues from Leo')
    try:
        response = requests.get(mensa_uri);
    except requests.exceptions.Timeout as timeOutException:
        logging.error('Could not get Information from STW-Muenster.de: '+timeOutException.message)
        return

    menue = ElementTree.fromstring(response.content)
    logging.debug(response.content)
    menueMessage = []

    try:
        for menuePerDate in menue:
            unixtimestamp = float(menuePerDate.attrib.get('timestamp'))
            lunchDate = datetime.datetime.fromtimestamp(unixtimestamp).date()
            if lunchDate == datetime.datetime.now().date():
                dishes = list(menuePerDate.iter('item'))
                for dish in dishes:
                    meal = dish.find('meal').text
                    mealIcon = dish.find('foodicons')
                    mealCategory = dish.find('category').text
                    mealDescription = meal + ' *Tagesaktion*' if mealCategory == 'Tagesaktion' else meal

                    # Python EAFP concept
                    icons = []
                    if mealIcon is not None and mealIcon.text is not None:
                        ingredients = mealIcon.text.split(',')
                        for i in ingredients:
                            try:
                                icons.append(foodIcons[str.lower(i.strip())])
                            except KeyError as keyErr:
                                logging.error('We have no mapping in our foodIcons for the ' + i.strip() + ' icon: '
                                              + keyErr.message)
                    iconText = None
                    if len(icons) == 0:
                        if mealCategory == 'Dessertbuffet':
                            iconText = ':ice_cream: '
                        else:
                            iconText = ':question: '
                    else:
                        iconText = ''.join(icons)
                    mealDescription = iconText + mealDescription

                    menueMessage.append(mealDescription)
    except Exception:
        logging.error(traceback.format_exc())
        # Logs the error appropriately.
    return menueMessage
