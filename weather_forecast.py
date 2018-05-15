import requests
from bs4 import BeautifulSoup
import re

"""
    Austin O'Donnell - Weather Forecast Script
    Program that browses the web for the current weather forecast
    by the given zipcode. Currently only works in the United States.
    Works in the background as a scheduled task in
    Windows 8.1/10 or as a command line script.
    Offers desktop GUI to show the current 7 day forecast or today's forecast
"""

days_of_the_week = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                    4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

def get_weekly_forecast(zipcode):

    url = url_by_zip(zipcode)
    weather_soup = access_weather_site(url)

    # Both used for the weekly forecast on the website. They are the same
    # length so they are able to be indexed simultaneously
    seven_day_forecasts = weather_soup.select('.short-desc')
    temp_extremes = weather_soup.select('.temp')

    forecasts = []
    for i in range(len(seven_day_forecasts)):
        forecasts.append({'forecast': ' '.join([x for x in seven_day_forecasts[i].contents if str(x) != '<br/>']),
                                  'extrema': temp_extremes[i].text})

    return forecasts


def get_todays_forecast(zipcode):

    url = url_by_zip(zipcode)
    weather_soup = access_weather_site(url)

    sky_cast = weather_soup.select('.myforecast-current')[0].text
    temp = weather_soup.select('.myforecast-current-lrg')[0].text
    table = weather_soup.select('#current_conditions_detail')[0].find_all('tr')
    humidity = table[0].contents[3].text
    wind_speed = table[1].contents[3].text

    return temp, sky_cast, humidity, wind_speed


def url_by_zip(zipcode):

    coords_url = 'https://gist.githubusercontent.com/erichurst/7882666/raw/'
    coords_site = requests.get(coords_url)
    coords_site.raise_for_status()
    regex = re.compile(str(zipcode) + r',( ?-?\d{2}\.\d{6}), ?(-?\d{2,3}\.\d{6})')
    lat, long = regex.search(coords_site.text).groups()
    return 'https://forecast.weather.gov/MapClick.php?lat={0}&lon={1}'.format(lat, long)


def access_weather_site(url):
    forecast_site = requests.get(url)
    forecast_site.raise_for_status()
    return BeautifulSoup(forecast_site.text, 'html.parser')


def main():
    print("Enter the zip-code of where you would like to look at the weather forecast : ")
    zipcode = int(input())
    todays_weather = get_todays_forecast(zipcode)
    print("Today's weather : ", todays_weather)
    weeks_weather = get_weekly_forecast(zipcode)
    for cast in weeks_weather:
        print(cast['forecast'], cast['extrema'], sep=', ')


if __name__ == '__main__':
    main()

