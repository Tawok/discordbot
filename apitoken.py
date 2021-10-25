import requests
from env_keys import *

def token_key():
        payload = {'grant_type':'client_credentials'}
        r = requests.post(f'https://us.battle.net/oauth/token', data=payload, auth=(client_key,client_pass)).json()
        token = r['access_token']
        return token

access_token = token_key()


if __name__ == '__main__':
    token_key()