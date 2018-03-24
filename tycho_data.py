from requests import get
from urllib.parse import urlencode
from config import API_KEY
import pandas as pd
import os
import csv
import time


def load_csv(file_name):
    with open(file_name) as f:
        return [{k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]


diseases = load_csv('diseases.csv')
cities = load_csv('cities.csv')

for disease in diseases:
    for city in cities:
        for event in ['cases', 'deaths']:
            file_name = 'data/' + \
                '_'.join([city['loc'], city['state'],
                          disease['disease'].replace('/', ' or ')]) + '.csv'
            if os.path.exists(file_name):
                continue
            query = urlencode({'loc_type': 'city', 'loc': city['loc'], 'disease': disease['disease'],
                               'event': event, 'state': city['state'],
                               'start': 1888, 'end': 2014, 'apikey': API_KEY}) + '.csv'
            r = get('http://www.tycho.pitt.edu/api/query?' + query, )

            size = len(r.content)
            print(r.url)
            print(size, disease, city)
            with open(file_name, 'wb') as f:
                if size <= 11 and 'No results' in r.text:
                    f.write(b"")
                else:
                    f.write(r.content)
