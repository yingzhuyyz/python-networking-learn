#!/usr/bin/env python3

from pygeocoder import Geocoder

if __name__ == '__main__':
   address = '2000 Simcoe Street North, Oshawa, Ontario'
   print(Geocoder.geocode(address)[0].coordinates)

