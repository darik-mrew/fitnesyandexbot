import requests
import os


def get_coordinates(address):
    response = requests.get(
        "https://geocode-maps.yandex.ru/1.x/",
        params={
            "format": "json",
            "geocode": address,
            'apikey': os.getenv('geocoder_apikey')
        },
    )
    response.raise_for_status()

    data = response.json()
    coordinates = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
    return float(coordinates[1]), float(coordinates[0])


def get_nearby_gyms(latitude, longitude):
    response = requests.get(
        "https://search-maps.yandex.ru/v1/",
        params={
            "text": "спортзал",
            'll': f'{longitude},{latitude}',
            "apikey": os.getenv('search_for_organizations_apikey'),
            "results": 3,
            'lang': 'ru_RU',
            'type': 'biz'
        },
    )
    response.raise_for_status()

    data = response.json()
    gyms = []
    for feature in data["features"]:
        coordinates = feature["geometry"]["coordinates"]
        gyms.append({
            "name": feature["properties"]["name"],
            "latitude": coordinates[1],
            "longitude": coordinates[0],
        })
    return gyms


def draw_map(user_latitude, user_longitude, gyms):
    params = {
        "ll": f"{user_longitude},{user_latitude}",
        "spn": "0.01,0.01",
        "pt": f'{user_longitude},{user_latitude},pm2rdl~' + '~'.join([f'{i["longitude"]},{i["latitude"]},pm2dbl' for i
                                                                      in gyms]),
        'apikey': os.getenv('static_api_apikey'),
        'l': 'map',
    }

    response = requests.get(
        "https://static-maps.yandex.ru/1.x/",
        params=params,
    )
    response.raise_for_status()

    return response.content
