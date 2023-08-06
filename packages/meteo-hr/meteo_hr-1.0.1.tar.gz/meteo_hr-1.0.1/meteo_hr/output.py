from meteo_hr import Place
from meteo_hr.parse import Forecast
from typing import Generator


def print_forecast(place: Place, data: Generator[Forecast, None, None]):
    day = None
    print(bold(place.name))

    for forecast in data:
        if day != forecast.day:
            print()
            print(bold(f"{forecast.day}"))
            day = forecast.day

        weather_icon = WEATHER_ICONS.get(forecast.weather_description)
        weather_icon = f"{weather_icon}" if weather_icon else "??"

        wind_icon = WINDS.get(forecast.wind_directon, "?")
        temperature = f"{forecast.temperature:>3}°C"
        if forecast.temperature >= 30:
            temperature = red(temperature)
        if forecast.temperature <= 0:
            temperature = blue(temperature)

        percipitation = f"{forecast.percipitation:>4}mm"
        if forecast.percipitation < 1:
            percipitation = gray(percipitation)
        if forecast.percipitation > 5:
            percipitation = yellow(percipitation)
        if forecast.percipitation > 10:
            percipitation = red(percipitation)

        print(" ".join([
            f"  {forecast.time:>5}  {temperature}  {percipitation}  {wind_icon}  {weather_icon}",
            f"{forecast.weather_description},",
            f"vjetar {forecast.wind_description}"
        ]))


def bold(string):
    return f"\033[1m{string}\033[0m"


def gray(string):
    return f"\033[90m{string}\033[0m"


def red(string):
    return f"\033[31m{string}\033[0m"


def yellow(string):
    return f"\033[33m{string}\033[0m"


def blue(string):
    return f"\033[34m{string}\033[0m"


WINDS = {
    "C0": gray("-"),
    "N1": gray("↓"),
    "S1": gray("↑"),
    "E1": gray("←"),
    "W1": gray("→"),
    "NE1": gray("↙"),
    "NW1": gray("↘"),
    "SE1": gray("↖"),
    "SW1": gray("↗"),
    "N2": yellow("↓"),
    "S2": yellow("↑"),
    "E2": yellow("←"),
    "W2": yellow("→"),
    "NE2": yellow("↙"),
    "NW2": yellow("↘"),
    "SE2": yellow("↖"),
    "SW2": yellow("↗"),
    "N3": red("↓"),
    "S3": red("↑"),
    "E3": red("←"),
    "W3": red("→"),
    "NE3": red("↙"),
    "NW3": red("↘"),
    "SE3": red("↖"),
    "SW3": red("↗"),
}


def print_weater_icons():
    print("black sun with rays", "\N{black sun with rays}", "\N{black sun with rays}\uFE0F")
    print("cloud with lightning", "\N{cloud with lightning}", "\N{cloud with lightning}\uFE0F")
    print("cloud with rain", "\N{cloud with rain}", "\N{cloud with rain}\uFE0F")
    print("cloud with snow", "\N{cloud with snow}", "\N{cloud with snow}\uFE0F")
    print("cloud", "\N{cloud}", "\N{cloud}\uFE0F")
    print("fog", "\N{fog}", "\N{fog}\uFE0F")
    print("sun behind cloud", "\N{sun behind cloud}", "\N{sun behind cloud}\uFE0F")
    print("sun with face", "\N{sun with face}", "\N{sun with face}\uFE0F")
    print("thunder cloud and rain", "\N{thunder cloud and rain}", "\N{thunder cloud and rain}\uFE0F")
    print("white sun behind cloud with rain", "\N{white sun behind cloud with rain}", "\N{white sun behind cloud with rain}\uFE0F")
    print("white sun behind cloud", "\N{white sun behind cloud}", "\N{white sun behind cloud}\uFE0F")
    print("white sun with small cloud", "\N{white sun with small cloud}", "\N{white sun with small cloud}\uFE0F")
    print("wind blowing face", "\N{wind blowing face}", "\N{wind blowing face}\uFE0F")


WEATHER_ICONS = {
    "magla, malo do umjereno oblačno": "\N{fog}\N{fog}",
    "magla, nebo vedro": "\N{fog}\uFE0F",
    "malo oblačno, danju sunčano": "\N{white sun with small cloud}\uFE0F",
    "oblačno i maglovito": "\N{cloud}\uFE0F",
    "oblačno uz malu količinu kiše te moguću grmljavinu": "\N{white sun behind cloud with rain}\uFE0F",
    "oblačno uz malu količinu kiše": "\N{white sun behind cloud with rain}\uFE0F",
    "oblačno uz umjerenu količinu kiše te moguću grmljavinu": "\N{cloud with rain}\uFE0F",
    "oblačno uz umjerenu količinu kiše": "\N{cloud with rain}\uFE0F",
    "oblačno uz znatnu količinu kiše te moguću grmljavinu": "\N{thunder cloud and rain}\uFE0F",
    "oblačno uz znatnu količinu kiše": "\N{cloud with rain}\uFE0F",
    "oblačno": "\N{cloud}\uFE0F",
    "pretežno oblačno": "\N{cloud}\uFE0F",
    "promjenljivo oblačno uz malu količinu kiše": "\N{white sun behind cloud with rain}\uFE0F",
    "promjenljivo oblačno uz moguću grmljavinu": "\N{cloud with lightning}\uFE0F",
    "promjenljivo oblačno uz umjerenu količinu kiše te moguću grmljavinu": "\N{white sun behind cloud with rain}\uFE0F",
    "promjenljivo oblačno uz umjerenu količinu kiše": "\N{white sun behind cloud with rain}\uFE0F",
    "promjenljivo oblačno uz uz malu količinu snijega": "\N{cloud with snow}\uFE0F",
    "promjenljivo oblačno uz znatnu količinu kiše": "\N{white sun behind cloud with rain}\uFE0F",
    "umjereno oblačno": "\N{sun behind cloud}\uFE0F",
    "vedro, danju sunčano": "\N{black sun with rays}\uFE0F",
}
