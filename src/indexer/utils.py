
import requests

def fetch_profile_tzkt(address):
    data = requests.get('https://api.tzkt.io/v1/accounts/' + address)
    profile = {
        'address': address,
        'name': ''
    }
    if data:
        data = data.json()
        if 'metadata' in data:
            if 'alias' in data['metadata']:
                profile['name'] = data['metadata']['alias']

    return profile
