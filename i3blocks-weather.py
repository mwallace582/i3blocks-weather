#!/usr/bin/env python

# All Hex Codes from https://erikflowers.github.io/weather-icons/

import os
import forecastio
from geopy.geocoders import Nominatim

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
    parser.add_option('-a', '--address', dest='address',
                      action='store', help='Your address')

    (options, args) = parser.parse_args()

    #Check options
    if not options.api_key:
        raise RuntimeError('A Dark Sky API key is required. Go to darksky.net/dev')
    if options.farenheit and options.celsius:
        raise RuntimeError('Only one degree unit may be specified')

    return options

def get_ip_location():
    import requests
    import json

    send_url = 'http://ip-api.com/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['lat']
    lon = j['lon']
    location = "{}, {}".format(j['city'], j['region'])
    return (lat, lon, location)

def get_addr_location(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude, address)

def convert_temp(options, temp):
    #Default is Farenheit
    if options.celsius:
        temp = round((temp - 32) * 5/9)
    elif options.farenheit:
        temp = round(temp)
    else:
        raise RuntimeError('A degree unit must be specified')
    return temp

def get_current_forecast(options, forecast):
    currently = forecast.currently()

    temp = convert_temp(options, currently.temperature)

    icon_str = currently.icon

    return (temp, icon_str)

def get_daily_forecast(options, forecast):
    daily = forecast.daily()
    return daily.summary

def get_hourly_forecast(options, forecast):
    hourly = forecast.hourly()
    return hourly.summary

def notify_forecast(location, daily_summary, hourly_summary):
    import subprocess
    title = u"Weather - {}".format(location)
    message = u"Hourly Summary:\n{0}\n\n".format(hourly_summary)
    message += u"Daily Summary:\n{0}".format(daily_summary)
    subprocess.Popen(['notify-send', title, message])

options = get_options()

if options.address:
    (lat, lon, location) = get_addr_location(options.address)
else:
    (lat, lon, location) = get_ip_location()

forecast = forecastio.load_forecast(options.api_key, lat, lon)
(temp, icon_str) = get_current_forecast(options, forecast)

FARENHEIT_HEX = 'f045'
CELSIUS_HEX   = 'f03c'

def get_icon_hex(options, icon_str):
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

(degrees_hex, icon_hex) = get_icon_hex(options, icon_str)

buttonPressed = os.environ.get('BLOCK_BUTTON', None)
if buttonPressed:
    daily_summary = get_daily_forecast(options, forecast)
    hourly_summary = get_hourly_forecast(options, forecast)
    notify_forecast(location, daily_summary, hourly_summary)

print("<span font='Weather Icons'>&#x{0}; {1}&#x{2};</span>".format(icon_hex, temp, degrees_hex))
