import re

from bs4 import BeautifulSoup, Tag
from decimal import Decimal
from typing import Generator, NamedTuple


class Forecast(NamedTuple):
    day: str
    time: str
    percipitation: Decimal
    temperature: int
    weather_description: str
    wind_description: str
    wind_directon: str


def parse_forecast(html) -> Generator[Forecast, None, None]:
    doc = BeautifulSoup(html, "html.parser")
    full_table = doc.select_one(".table-weather-7day")
    mobile_table = doc.select_one(".fd-u-display--block .table-weather-7day")

    if not full_table or not mobile_table:
        raise ParseError()

    matches = re.findall(r"\[new Date\(\d+,\d+,\d+,\d+\),(-?\d+),([0-9.]+)\]", html)
    temp_percs = ((int(t), Decimal(p)) for t, p in matches)

    times = day_time_gen(mobile_table)
    winds = wind_gen(full_table)
    weathers = weather_gen(full_table)

    for (
        (day, time),
        (wind_icon, wind_description),
        weather_description,
        (temperature, percipitation)
    ) in zip(times, winds, weathers, temp_percs):
        yield Forecast(
            day,
            time,
            percipitation,
            temperature,
            weather_description,
            wind_description,
            wind_icon,
        )


def wind_gen(full_table: Tag):
    images = full_table.select("td > span > img.fd-c-iconsvg--7dwind")
    for image in images:
        assert image.parent is not None
        description = image.parent.attrs["title"]
        icon = image.attrs["src"].split("/")[-1].replace(".svg", "")
        yield icon, description


def weather_gen(full_table: Tag):
    images = full_table.select("td > span > img:not(.fd-c-iconsvg--7dwind)")
    for image in images:
        assert image.parent is not None
        yield image.parent.attrs["title"]


def day_time_gen(mobile_table: Tag):
    day = None
    ths = mobile_table.select("th")
    for th in ths:
        if th.attrs.get("colspan") == "4":
            day = th.text

        if re.match(r"\d+:\d+", th.text):
            assert day is not None
            yield day, th.text


class ParseError(Exception):
    pass
