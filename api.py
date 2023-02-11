import io
from typing import Optional, Tuple

import requests
from PIL import Image
from enum import Enum


class ApiException(Exception):
    pass


class GettingMapError(ApiException):
    pass


class LocationNotFoundError(ApiException):
    pass


class PointError(ApiException):
    pass


class Scheme(Enum):
    Sattelite = "sat"
    Map = "map"
    Hybrid = "sat,skl"


URL = f"https://static-maps.yandex.ru/1.x"

DEFAULT_LOCATION = 37.620070, 55.753630
MAP_SIZE = 650, 450
DEFAULT_ZOOM = 10
DEFAULT_STEP = 0.1
DEFAULT_SCHEME = Scheme.Hybrid


class Style(Enum):
    # Styles supporting colors and sizes
    Rect = "pm"
    Circle = "pm2"
    Flag = "flag"
    Pin = "vk"

    # Vector styles, colors and sizes unsupported
    Org = "org"
    Comma = "comma"
    Round = "round"
    Home = "home"
    Work = "work"
    Yandex = "ya_ru"


class Color(Enum):
    White = "wt"
    DarkOrange = "do"
    DarkBlue = "db"
    Blue = "bl"
    Green = "gn"
    DarkGreen = "dg"
    Grey = "gr"
    LightBlue = "lb"
    Night = "nt"
    Orange = "or"
    Pink = "pn"
    Red = "rd"
    Violet = "vv"
    Yellow = "yw"
    A = "a"
    B = "b"
    EmptyViolet = "dir"
    BlueYellow = "blyw"


class Size(Enum):
    Small = "s"
    Medium = "m"
    Large = "l"


_AVAILABLES = {
    "pm": {"colors": "wtdodbblgngrlbntorpnrdvvywab", "sizes": "sml"},
    "pm2": {"colors": "wtdodbblgndggrlbntorpnrdvvywaborgdirblyw", "sizes": "ml"},
    "flag": {"colors": "", "sizes": ""},
    "vk": {"colors": "bkgr", "sizes": "m"},
    "org": {"colors": "", "sizes": ""},
    "comma": {"colors": "", "sizes": ""},
    "round": {"colors": "", "sizes": ""},
    "home": {"colors": "", "sizes": ""},
    "work": {"colors": "", "sizes": ""},
    "ya_ru": {"colors": "", "sizes": ""},
}


class Point:
    def __init__(
        self,
        coords: Tuple[float, float],
        style: Style = Style.Flag,
        color: Optional[Color] = None,
        size: Optional[Size] = None,
        content: Optional[int] = None,
    ):
        self.coords = coords
        self.style = style
        self.color = color
        self.size = size
        self.content = content

        self._check_conflicts()

    def _check_conflicts(self):
        a = _AVAILABLES[self.style.value]
        colors, sizes = a["colors"], a["sizes"]

        if self.color and self.color.value not in colors:
            raise PointError(f"{self.color} conflicts with {self.style}")

        if self.size and self.size.value not in sizes:
            raise PointError(f"{self.size} conflicts with {self.style}")

        if not self.content:
            return

        if self.style.value in "flagvkorgcommaroundhomeworkya_ru":
            raise PointError(f"Content assignment not supported by {self.style}")

        if self.style == Style.Rect and self.size:
            if self.size in {Size.Small, Size.Medium} and not (1 <= self.content <= 99):
                raise PointError(f"{self.content} must be in range [1,99]")
            if self.size == Size.Large and not (1 <= self.content <= 100):
                raise PointError(f"{self.content} must be in range [1,100]")
        elif self.style == Style.Circle and not (1 <= self.content <= 99):
            raise PointError(f"{self.content} must be in range [1,99]")

    def desc(self) -> str:
        color = self.color.value if self.color else ""
        size = self.size.value if self.size else ""
        content = self.content if self.content else ""

        return f"{self.coords[0]},{self.coords[1]},{self.style.value}{color}{size}{content if content else ''}"

    def __str__(self):
        return self.desc()


# Usage example:
# get_map(-25.694422, 133.791467, (25, 35), scheme=Scheme.Map)
def get_map(
    coords=DEFAULT_LOCATION,
    zoom=DEFAULT_ZOOM,
    scheme=DEFAULT_SCHEME,
    points=None,
):
    url = f"{URL}/?ll={coords[0]},{coords[1]}&z={zoom}&size={MAP_SIZE[0]},{MAP_SIZE[1]}&l={scheme.value}"

    if points and type(points) is Point:
        url += f"&pt={points.desc()}"
    elif points:
        url += f"&pt={'~'.join(map(Point.desc, points))}"

    try:
        if response := requests.get(url):
            return Image.open(io.BytesIO(response.content))
    except Exception:
        pass

    raise GettingMapError


_LOC_CACHE = {}
_LOC_LAST = None


def locate(address: str):
    url = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&"
    params = {
        "geocode": address,
        "format": "json",
    }

    if address in _LOC_CACHE:
        return _LOC_CACHE[address]

    try:
        global _LOC_LAST
        if response := requests.get(url, params=params):
            response_json = response.json()

            toponym = response_json["response"]["GeoObjectCollection"]["featureMember"][
                0
            ]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]

            coords = tuple(map(float, toponym_coodrinates.split(" ")))
            _LOC_CACHE[address] = coords
            _LOC_LAST = coords
            return coords
        return _LOC_LAST if _LOC_LAST else DEFAULT_LOCATION
    except requests.RequestException:
        raise LocationNotFoundError
    except IndexError:
        raise LocationNotFoundError
