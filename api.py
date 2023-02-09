import io

import requests
from PIL import Image
from enum import Enum
from PIL.ImageQt import ImageQt

URL = f"https://static-maps.yandex.ru/1.x"


class Scheme(Enum):
    Sattelite = "sat"
    Map = "map"
    Hybrid = "sat,skl"


# Пример использования:
# get_map(-25.694422, 133.791467, (25, 35), scheme=Scheme.Map)
def get_map(latitude, longitude, scheme=Scheme.Hybrid):
    url = f"{URL}/?ll={longitude},{latitude}&size=650,450&l={scheme.value}&spn=25,35"
    if response := requests.get(url):
        return ImageQt(Image.open(io.BytesIO(response.content)))

    raise requests.ConnectionError


def locate(address: str) -> str or None:
    url = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&"
    params = {
            'geocode': address,
            'format': 'json',
            }

    if response := requests.get(url, params=params):
        response_json = response.json()

        toponym = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates
    else:
        return
