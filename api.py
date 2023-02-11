import io

import requests
from PIL import Image
from enum import Enum

URL = f"https://static-maps.yandex.ru/1.x"


class ApiException(Exception):
    pass


class GettingMapError(ApiException):
    pass


class LocationNotFoundError(ApiException):
    pass


class Scheme(Enum):
    Sattelite = "sat"
    Map = "map"
    Hybrid = "sat,skl"


DEFAULT_LOCATION = 37.620070, 55.753630
MAP_SIZE = 650, 450
DEFAULT_ZOOM = 10
DEFAULT_STEP = 0.1

# Пример использования:
# get_map(-25.694422, 133.791467, (25, 35), scheme=Scheme.Map)
def get_map(coords=DEFAULT_LOCATION, zoom=DEFAULT_ZOOM, scheme=Scheme.Hybrid):
    url = f"{URL}/?ll={coords[0]},{coords[1]}&z={zoom}&size={MAP_SIZE[0]},{MAP_SIZE[1]}&l={scheme.value}"

    try:
        if response := requests.get(url):
            return Image.open(io.BytesIO(response.content))
    except Exception:
        pass

    raise GettingMapError


_LOC_CACHE = {}


def locate(address: str):
    url = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&"
    params = {
        "geocode": address,
        "format": "json",
    }

    if address in _LOC_CACHE:
        return _LOC_CACHE[address]

    try:
        if response := requests.get(url, params=params):
            response_json = response.json()

            toponym = response_json["response"]["GeoObjectCollection"]["featureMember"][
                0
            ]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]

            coords = toponym_coodrinates.split(" ")
            _LOC_CACHE[address] = coords
        return ()
    except requests.RequestException:
        raise LocationNotFoundError
    except IndexError:
        raise LocationNotFoundError
