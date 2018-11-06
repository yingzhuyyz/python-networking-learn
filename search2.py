#!/usr/bin/env python3

import requests
import os

def geocode(address):
    parameters = {'address': address, 'sensor': 'false', 'key': os.environ['GOOGLE_API_KEY']}
    base = 'https://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get(base, params=parameters)
    answer = response.json()
    print(answer['results'][0]['geometry']['location'])

if __name__ == '__main__':
    geocode('2000 Simcoe Street North, Oshawa, Ontario')

