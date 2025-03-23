import requests
from pprint import pprint

account_id = 1170923497
headers = {'accept': 'application/json'}
params = {'limit': 20}

response = requests.get(f'https://api.opendota.com/api/players/{account_id}', headers=headers, params=params)

data = response.json()
pprint(data)
