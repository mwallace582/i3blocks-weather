# Weather for i3blocks

A simple python script which uses the [Pirate Weather API](https://pirateweather.net/) to
get location based weather information to display in [i3blocks](https://github.com/vivien/i3blocks).

You will need a Pirate Weather API key, which is free and can be obtained
easily from the Pirate Weather site. API requests are limited to 20,000 calls
per month per key, so running the command every 15 minutes will keep you under
that limit presuming it will be running 24/7.

If a location is not provided via the command line, the script will
automatically locate you using your IP address. This obviously doesn't work if
you use a VPN. In that case, you must specify your location on the command
line.

Location data is provided by [IP-API.com](http://ip-api.com/). They
automatically ban any IP address that exceeds 150 requests per minute. You've
been warned.

This utility depends on the [Weather Icons](http://erikflowers.github.io/weather-icons/)
font package and [python-forecastio](https://github.com/ZeevG/python-forecast.io).

Add the following to your `i3blocks.conf` file:
```
[Weather]
command=/path/to/i3blocks-weather.py -f -k <pirate_weather_api_key>
markup=pango
interval=100
```

# Dependencies

```
pip install geopy
pip install python-forecastio
```
