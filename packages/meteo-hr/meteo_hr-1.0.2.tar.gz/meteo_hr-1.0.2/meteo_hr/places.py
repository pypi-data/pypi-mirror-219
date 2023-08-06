import locale
from typing import List
from . import Place3D, Place7D, cache, api


# Required for locale-aware sorting
locale.setlocale(locale.LC_ALL, "hr_HR.utf8")


def list_3d() -> List[Place3D]:
    places = cache.load_3d()
    if not places:
        places = api.fetch_places_3d()
        places = sorted(places, key=lambda p: locale.strxfrm(p.name))
        cache.save_3d(places)
    return places


def list_7d() -> List[Place7D]:
    places = cache.load_7d()
    if not places:
        places = api.fetch_places_7d()
        places = sorted(places, key=lambda p: locale.strxfrm(p.name))
        cache.save_7d(places)
    return places
