import requests
from env_keys import *
from apitoken import access_token

class Ratings:
    def __init__(self, character):
        self.character = character

    def rating_rbg(self):
        args = {'namespace':'profile-us', 'locale':'en_US', 'access_token': access_token}
        url = f'https://us.api.blizzard.com/profile/wow/character/sargeras/{self.character}/pvp-bracket/rbg'
        r1 = requests.get(url, params=args).json()
        r1_rating = r1['rating']
        return r1_rating

    def rating_2v2(self):
        args = {'namespace':'profile-us', 'locale':'en_US', 'access_token': access_token}
        url = f'https://us.api.blizzard.com/profile/wow/character/sargeras/{self.character}/pvp-bracket/2v2'
        r1 = requests.get(url, params=args).json()
        r1_rating = r1['rating']
        return r1_rating

    def rating_3v3(self):
        args = {'namespace':'profile-us', 'locale':'en_US', 'access_token': access_token}
        url = f'https://us.api.blizzard.com/profile/wow/character/sargeras/{self.character}/pvp-bracket/3v3'
        r1 = requests.get(url, params=args).json()
        r1_rating = r1['rating']
        return r1_rating


tawok = Ratings('tawok')
antef = Ratings('antef')
femiane = Ratings('femiane')
arreolâ = Ratings('arreolâ')
vainx = Ratings('vainx')
gurab = Ratings('gurab')
daralian = Ratings('daralian')
Jackoblades = Ratings('Jackoblades')
jinlike = Ratings('jinlike')