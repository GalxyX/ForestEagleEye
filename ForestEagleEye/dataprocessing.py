import requests

API_KEY = "a4ff6e3b16fa5bc76d719f465c90e6da"

city = "110000"

#extensions = "all"

url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={API_KEY}&city={city}&extensions=all&output=JSON"

response = requests.get(url)

data = response.json()

print(data)

s_city = data["forecasts"][0]["city"]
s_date = data["forecasts"][0]["casts"][0]["date"]
s_dayweather = data["forecasts"][0]["casts"][0]["dayweather"]
s_daytemp = data["forecasts"][0]["casts"][0]["daytemp"]

print(f"城市: {s_city}")
print(f"日期: {s_date}")
print(f"白天天气: {s_dayweather}")
print(f"白天温度: {s_daytemp}")
