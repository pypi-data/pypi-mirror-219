import argparse
import logging
import sys

from difflib import SequenceMatcher
from meteo_hr import cache
from meteo_hr.api import fetch_forecast_html
from meteo_hr.output import print_forecast
from meteo_hr.parse import parse_forecast
from meteo_hr.places import list_3d, list_7d


def make_parser():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("place", nargs="*", type=str)
    parser.add_argument("-l", "--list", action="store_true")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-7", "--week", action="store_true")
    parser.add_argument("-c", "--clear-cache", action="store_true")
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.clear_cache:
        cache.clear()

    places = list_7d() if args.week else list_3d()

    if args.list:
        for place in places:
            print(place.name)
        return

    place_name = " ".join(args.place).lower()

    if not place_name:
        print("Place is required.", file=sys.stderr)
        sys.exit(1)

    place = max(places, key=lambda p: name_diff(p.name, place_name))
    diff = name_diff(place.name, place_name)

    if diff < 0.5:
        print("Place not found", file=sys.stderr)
        sys.exit(1)

    forecast = fetch_forecast_html(place)
    parsed = parse_forecast(forecast)
    print_forecast(place, parsed)


def name_diff(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
