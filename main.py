import requests
from flask import Flask, render_template

app = Flask(__name__)

# Укажите ваш ключ API
api_key = "	2uH0vFWOElk8IFBqLPAfVn7I3aOMTBtT"

# URL для поиска местоположения (Лондон)
location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q=London"

# Получаем ключ местоположения для Лондона
location_response = requests.get(location_url)
if location_response.status_code == 200:
    location_data = location_response.json()
    if location_data:
        location_key = location_data[0]['Key']  # Получаем ключ местоположения
    else:
        print("Не удалось найти местоположение.")
        exit()
else:
    print(f"Ошибка при получении местоположения: {location_response.status_code}")
    exit()

# URL для получения текущей погоды
weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"

# Получаем текущую погоду
weather_response = requests.get(weather_url)
if weather_response.status_code == 200:
    weather_data = weather_response.json()
    current_weather = weather_data[0]

    # Выводим информацию о погоде
    print(f"Текущая погода в Лондоне:")
    print(f"Температура: {current_weather['Temperature']['Metric']['Value']}°C")
    print(f"Состояние: {current_weather['WeatherText']}")
else:
    print(f"Ошибка при получении погоды: {weather_response.status_code}")

@app.route('/', methods=['GET'])
def main():
    return render_template('main_page.html')

if __name__ == '__main__':
    app.run()