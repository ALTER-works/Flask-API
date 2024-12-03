import requests
from flask import Flask, render_template, request

app = Flask(__name__)

api_key = "2uH0vFWOElk8IFBqLPAfVn7I3aOMTBtT"


def get_location_key(city):
    # URL для поиска местоположения
    location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city}"
    location_response = requests.get(location_url)
    if location_response.status_code == 200:
        location_data = location_response.json()
        if location_data:
            return location_data[0]['Key']  # Возвращаем ключ местоположения
    return None


def get_current_weather(location_key):
    # URL для получения текущей погоды
    weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"
    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        return weather_data[0]  # Возвращаем данные о погоде
    return None


@app.route('/', methods=['GET', 'POST'])
def main():
    weather_info = None
    if request.method == 'POST':
        city = request.form['city']
        location_key = get_location_key(city)
        if location_key:
            weather_info = get_current_weather(location_key)
        else:
            weather_info = {"error": "Не удалось найти местоположение."}

    return render_template('main_page.html', weather_info=weather_info)


if __name__ == '__main__':
    app.run(debug=True)