NOT READY

import json
import requests

page = 0

request = requests.get('https://api.hh.ru/vacancies/',
                       headers={'User-Agent': 'Python (fuoff@gmail.com)'},
                       params={
                           'text': 'python junior',
                           'page': page,
                           'per_page': '100'
                       })

json_responce = request.json()

for i in json_responce['items']:
    print(i)
