import requests
import os

from dotenv import load_dotenv


load_dotenv()

# https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f?permalink_comment_id=3769668#gistcomment-3769668


def calculate_bearing(d):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = int(round(d / (360. / len(dirs))))
    return dirs[ix % len(dirs)]


def checkAPIKey(API_KEY: str) -> bool:
    data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat=22.51829&lon=88.362951&appid={API_KEY}&units=Metric")
    if data.status_code == 200:
        return True
    else:
        return False


def geoCode(location: str):
    location = location.replace(" ", "+")
    try:
        data = requests.get(
            f"http://api.positionstack.com/v1/forward?access_key={os.getenv('latlonAPIKEY')}&query={location}&limit=1")
        lon = data.json()["data"][0]["longitude"]
        lat = data.json()["data"][0]["latitude"]
        region = data.json()["data"][0]["region"] 
        street = data.json()["data"][0]["street"]
        country = data.json()["data"][0]["country"]
        county = data.json()["data"][0]["county"]
        coordinates = {"lat": lat, "lon": lon, "region":region,"street":street,"country":country,"county":county}
    except Exception:
        lon = lat = coordinates = None
    return coordinates


class weatherServices:

    temp = None
    weatherCondition = None
    minTemp = None
    maxTemp = None
    feelsLike = None
    humidity = None
    windSpeed = None
    windDirection = None
    icon = None
    location = None
    unitText = None
    sunriseAt = None
    sunsetAt = None
 

    def __init__(self, api_key: str, lat: str, lon: str, units: str):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.units = units

    def getData(self):
        if self.units == 'Metric':
            self.unitText = '°C'
        else:
            self.unitText = '°F'
        data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units={self.units}")
        self.temp = str(round(float(data.json()["main"]["temp"])))
        self.weatherCondition = data.json()["weather"][0]["main"]
        self.minTemp = data.json()["main"]["temp_min"]
        self.maxTemp = data.json()["main"]["temp_max"]
        self.humidity = data.json()["main"]["humidity"]
        self.windSpeed = data.json()["wind"]["speed"]
        self.windDirection = calculate_bearing(int(data.json()["wind"]["deg"]))
        self.icon = data.json()["weather"][0]["icon"]
        self.feelsLike = str(round(float(data.json()["main"]["feels_like"])))
        self.location = data.json()["name"]
        self.sunriseAt = data.json()["sys"]["sunrise"]
        self.sunsetAt = data.json()["sys"]["sunset"]