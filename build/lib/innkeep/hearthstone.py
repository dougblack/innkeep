import requests


BASE_URI = 'https://api.hearthstonejson.com/v1/'

class HSResource(object):
    """
    This object represents a resource in the Hearthstone API.
    """
    location = None

    def __init__(self):
        pass

    def all(self, **params):
        uri = BASE_URI + '25770/enUS/cards.json'
        return requests.get(uri, params=params).json()


class Cards(HSResource):
    pass
