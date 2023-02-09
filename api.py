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
    print(url)
    if response := requests.get(url):
        return ImageQt(Image.open(io.BytesIO(response.content)))

    raise requests.ConnectionError
