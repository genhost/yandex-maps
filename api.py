import io

import requests
from PIL import Image
from enum import Enum

URL = f"https://static-maps.yandex.ru/1.x/"


class Scheme(Enum):
    Sattelite = "sat"
    Map = "map"
    Hybrid = "sat,skl"


# Пример использования:
# get_map(-25.694422, 133.791467, (25, 35), scheme=Scheme.Map)
def get_map(latitude, longitude, size, scheme=Scheme.Hybrid):
    params = {"ll": (longitude, latitude), "spn": size, "l": scheme.value}

    if response := requests.get(URL, params=params):
        return Image.open(io.BytesIO(response.content))

    raise requests.ConnectionError
