import requests

from bs4 import BeautifulSoup
from typing import List, Generator
from meteo_hr import Place, Place3D, Place7D


def gen_places_3d() -> Generator[Place3D, None, None]:
    response = requests.get("https://meteo.hr/prognoze.php", params={
        "section": "prognoze_model",
        "param": "3d",
    })
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    groups = soup.select(".city-picker__select optgroup")

    for group in groups:
        region = group.attrs["label"].replace("ž.", "županija")
        for option in group.select("option"):
            name = option.text
            slug = option.attrs["value"]
            yield Place3D(name, slug, region)


def gen_places_7d() -> Generator[Place7D, None, None]:
    response = requests.get("https://meteo.hr/prognoze.php", params={
        "section": "prognoze_model",
        "param": "7d",
    })
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    options = soup.select(".city-picker__select option")

    for option in options:
        name = option.text
        code = option.attrs["value"]
        yield Place7D(name, code)


def fetch_places_3d() -> List[Place3D]:
    return list(gen_places_3d())


def fetch_places_7d() -> List[Place7D]:
    return list(gen_places_7d())


def fetch_forecast_html(place: Place):
    if isinstance(place, Place3D):
        return _fetch_forecast_3d(place)

    if isinstance(place, Place7D):
        return _fetch_forecast_7d(place)

    raise ValueError("Invalid place: {place}")


def _fetch_forecast_3d(place: Place3D):
    response = requests.get("https://meteo.hr/prognoze.php", params={
        "Code": place.slug,
        "id": "prognoza",
        "section": "prognoze_model",
        "param": "3d",
    })
    response.raise_for_status()
    return response.text


def _fetch_forecast_7d(place: Place7D):
    response = requests.get("https://meteo.hr/prognoze.php", params={
        "Code": place.code,
        "id": "prognoza",
        "section": "prognoze_model",
        "param": "7d",
    })
    response.raise_for_status()
    return response.text
