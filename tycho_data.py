from requests import get
from config import API_KEY
import pandas as pd
import os
import csv
import time


def load_csv(file_name):
    with open(file_name) as f:
        return [{k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]


conditions = load_csv('condition.csv')
cities = load_csv('city.csv')

for condition in conditions:
    for city in cities:
        offset = 0
        while True:
            file_name = 'data/' + \
                '_'.join(
                    [city['CityName'], condition['ConditionName'], str(offset)]) + '.csv'
            if os.path.exists(file_name):
                break
            params = {'ConditionName': condition['ConditionName'],
                      'CityName': city['CityName'].replace('.', '%2E'), 'apikey': API_KEY,
                      'limit': 20000, 'offset': offset}
            url = 'https://www.tycho.pitt.edu/api/query?limit=20000&offset=' + \
                str(offset) + '&apikey=' + API_KEY + '&ConditionName=' + \
                condition['ConditionName'] + '&CityName=' + city['CityName']
            r = get('https://www.tycho.pitt.edu/api/query', params=params)
            content = r.content
            size = len(content)
            empty = size <= 11 and 'No results' in r.text
            print(r.url)
            print(size, city['CityName'], condition['ConditionName'], offset)
            with open(file_name, 'wb') as f:
                if empty:
                    f.write(b"")
                else:
                    f.write(r.content)
            if empty:
                break
            else:
                offset += 20000
