#!/usr/bin/env python3

from pygeocoder import Geocoder
import os

if __name__ == '__main__':
   address = '2000 Simcoe Street North, Oshawa, Ontario'
   print(Geocoder(os.environ['GOOGLE_API_KEY']).geocode(address)[0].coordinates)

