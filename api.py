import io

import requests
from PIL import Image

SATELLITE = 'sat'
MAP = 'map'
HYBRID = 'sat,skl'


def get_map(latitude, longitude, size, l):
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&spn={size[0]},{size[1]}&l={l}"
    print(map_request)
    try:
        if response := requests.get(map_request):
            file = Image.open(io.BytesIO(response.content))
            return file
        else:
            raise StopIteration
    except StopIteration:
        print('НЕПРАВИЛЬНЫЙ ЗАПРОС')


file = get_map('-25.694422', '133.791467', ['25', '35'], MAP)
