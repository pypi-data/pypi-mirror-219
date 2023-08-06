meteo.hr CLI
============

Commandline tool for displaying the forecast from [meteo.hr](http://meteo.hr/prognoze.php?section=prognoze_model&param=3d).

Install:

```
pip install --user meteo_hr
```

Usage:

```
meteo <place>
```

For example:

```
meteo zagreb
```

![Forecast for Zagreb](forecast.png)

7 day forecast:

```
meteo zagreb -7
```


List available places for 3 day forecast:

```
meteo --list
```

List available places for 7 day forecast:

```
meteo --list
```
