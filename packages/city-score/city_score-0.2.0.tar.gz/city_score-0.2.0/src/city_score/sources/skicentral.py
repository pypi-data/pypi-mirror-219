from ..decorators import criterion, dimension, scorer
from ..source import Source

from geopy.distance import geodesic
import json

states = (
        'alaska', 'california', 'idaho', 'nevada', 'oregon', 'washington', 'arizona', 'colorado', 'montana', 'newmexico', 'utah', 'wyoming',
        'alabama', 'indiana', 'michigan', 'missouri', 'ohio', 'wisconsin', 'illinois', 'iowa', 'minnesota', 'northdakota', 'southdakota',
        'connecticut', 'massachusetts', 'newyork', 'vermont', 'maine', 'newhampshire', 'rhodeisland',
        'maryland', 'northcarolina', 'tennessee', 'newjersey', 'pennsylvania', 'virginia'
        )

class SkiCentral(Source):
    files = {'skicentral-%s.json' % s: {
            'url': 'https://www.skicentral.com/%s-map.html' % s,
            'pre_start': 'var mountains = ',
            'post_end': ';\n\ninfowindow = null;',
        } for s in states}

    @classmethod
    def populate(cls, cities):
        ski_resort_data = []

        for state in states:
            ski_resort_data += json.load(cls.open('skicentral-%s.json' % state))

        for city in cities.values():
            ski_resorts = []
            for datum in ski_resort_data:
                name = datum[0]
                lat = datum[2]
                lng = datum[3]

                if abs(lat - city.lat) >= 2: # one degree is approx. 69 miles
                    continue

                if abs(lng - city.lng) >= 2:
                    continue

                distance = geodesic(city.coordinates, (lat, lng))
                ski_resorts.append({
                    'name': name,
                    'miles': distance.miles
                })

            city.update({
                'ski_resorts': ski_resorts
            })

@dimension('Nearby ski resorts')
def nearby_ski_resorts(city, compact=False, miles=100, exclude=[]):
    if ski_resorts := city.data.get('ski_resorts'):
        if len(ski_resorts) == 0:
            return None

        ski_resorts = tuple(filter(lambda r: r['miles'] <= miles and r['name'] not in exclude, sorted(ski_resorts, key=lambda r: r['miles'])))
        f = '{resort[name]} ({resort[miles]:.0f} miles)'
        if compact:
            closest_resort = ski_resorts[0]
            s = f.format(resort=closest_resort)
            if len(ski_resorts) > 1:
                s += ' and %d more' % (len(ski_resorts) - 1)
            return s

        l = [f.format(resort=resort) for resort in ski_resorts]
        return '\n'.join(l)

    return None

@criterion('Minimum ski resorts')
def minimum_ski_resorts(city, count, miles=100, default=False, exclude=[]):
    if 'ski_resorts' not in city.data:
        return default

    nearby_ski_resorts = tuple(filter(lambda r: r['miles'] <= miles and r['name'] not in exclude, city.data['ski_resorts']))
    return len(nearby_ski_resorts) >= count

@scorer('Closest ski resort score')
def closest_ski_resort_scorer(city, lower, upper, exclude=[]):
    if ski_resorts := city.data.get('ski_resorts'):
        if len(ski_resorts) == 0:
            return 0
        
        ski_resorts = tuple(filter(lambda r: r['name'] not in exclude, sorted(ski_resorts, key=lambda r: r['miles'])))
        closest_resort_miles = ski_resorts[0]['miles']

        if closest_resort_miles <= lower:
            return 100
        if closest_resort_miles <= upper:
            return round((1 - (closest_resort_miles - lower) / (upper - lower)) * 100)
    
    return 0
