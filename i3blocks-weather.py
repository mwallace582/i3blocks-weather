#!/usr/bin/env python

# All Hex Codes from https://erikflowers.github.io/weather-icons/

import forecastio

def get_options():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-f', '--farenheit', dest='farenheit',
                      action='store_true', default=False,
                      help='Report degrees in Farenheit')
    parser.add_option('-c', '--celsius', dest='celsius',
                      action='store_true', default=False,
                      help='Report degrees in Celsius')
    parser.add_option('-k', '--api-key', dest='api_key',
                      action='store', help='Dark Sky API key')

    (options, args) = parser.parse_args()

    #Check options
    if not options.api_key:
        raise RuntimeError('A Dark Sky API key is required. Go to darksky.net/dev')
    if options.farenheit and options.celsius:
        raise RuntimeError('Only one degree unit may be specified')

    return options

def get_lat_lon():
    import requests
    import json

    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return (lat, lon)

def get_forecast(options, lat, lon):
    forecast = forecastio.load_forecast(options.api_key, lat, lon)

    currently = forecast.currently()

    #Default is Farenheit
    if options.celsius:
        temp = round((currently.temperature- 32) * 5/9)
    elif options.farenheit:
        temp = round(currently.temperature)
    else:
        raise RuntimeError('A degree unit must be specified')

    icon_str = currently.icon

    return (temp, icon_str)

options = get_options()

(lat, lon) = get_lat_lon()

(temp, icon_str) = get_forecast(options, lat, lon)

FARENHEIT_HEX = 'f045'
CELSIUS_HEX   = 'f03c'

def get_hex_codes(options, icon_str):
    if options.farenheit:
        degrees_hex = FARENHEIT_HEX
    elif options.celsius:
        degrees_hex = CELSIUS_HEX
    else:
        raise RuntimeError('A degree unit must be specified')

    if icon_str == 'clear-day':
        icon_hex='f00d'
    elif icon_str == 'clear-night':
        icon_hex='f02e'
    elif icon_str == 'rain':
        icon_hex='f019'
    elif icon_str == 'snow':
        icon_hex='f01b'
    elif icon_str == 'sleet':
        icon_hex='f0b5'
    elif icon_str == 'wind':
        icon_hex='f050'
    elif icon_str == 'fog':
        icon_hex='f014'
    elif icon_str == 'cloudy':
        icon_hex='f013'
    elif icon_str == 'partly-cloudy-day':
        icon_hex = 'f002'
    elif icon_str == 'partly-cloudy-night':
        icon_hex = 'f083'
    elif icon_str == 'thunderstorm':
        icon_hex = 'f016'
    elif icon_str == 'hail':
        icon_hex = 'f015'
    elif icon_str == 'tornado':
        icon_hex = 'f056'
    else:
        icon_hex = 'f07b' # N/A
    return (degrees_hex, icon_hex)

(degrees_hex, icon_hex) = get_hex_codes(options, icon_str)

line =  "<span font='Weather Icons'>&#x{0};</span> <span>{1}</span>".format(icon_hex, temp)
line += "<span font='Weather Icons'>&#x{0};</span>".format(degrees_hex)
print(line)
