import json
import logging
import os
import time

from meteo_hr import Place3D, Place7D


logger = logging.getLogger(__name__)

PLACES_3D_CACHE = "places_3d.json"
PLACES_7D_CACHE = "places_7d.json"
STALE_AFTER_SECONDS = 30 * 24 * 3600  # 30 days


def load_3d():
    places = _load(PLACES_3D_CACHE)
    if places:
        return [Place3D(*place) for place in places]


def save_3d(data):
    _save(PLACES_3D_CACHE, data)


def load_7d():
    places = _load(PLACES_7D_CACHE)
    if places:
        return [Place7D(*place) for place in places]


def save_7d(data):
    _save(PLACES_7D_CACHE, data)


def clear():
    logger.debug("Clearing cache")
    path_3d = _get_cache_path(PLACES_3D_CACHE)
    path_7d = _get_cache_path(PLACES_7D_CACHE)

    if os.path.exists(path_3d):
        os.unlink(path_3d)

    if os.path.exists(path_7d):
        os.unlink(path_7d)


def _load(filename):
    now = time.time()
    path = _get_cache_path(filename)

    if os.path.exists(path):
        modtime = os.path.getmtime(path)
        if now - modtime < STALE_AFTER_SECONDS:
            logger.debug(f"Loading cache from {path}")
            try:
                with open(path) as f:
                    return json.load(f)
            except Exception as ex:
                logger.exception(ex)
                return None
        else:
            logger.debug("Cache is stale")
    else:
        logger.debug("Cache not found")


def _save(path, data):
    path = _get_cache_path(path)
    logger.debug(f"Saving cache to {path}")
    with open(path, "w") as f:
        json.dump(data, f)


def _get_cache_dir():
    # TODO: handle windows, mac
    default_path = os.path.expanduser("~/.cache")
    cache_home = os.getenv("XDG_CACHE_HOME", default_path)
    cache_dir = os.path.join(cache_home, "meteo_hr")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def _get_cache_path(path) -> str:
    return os.path.join(_get_cache_dir(), path)
