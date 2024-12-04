import requests
from deep_translator import GoogleTranslator as GT
from flask import Flask, render_template, request

app = Flask(__name__)

api_key = "GRWpt0MH0CQnYoQXDqfMw1GrM0PT3u9f"

def get_location_key(city):
    # URL для поиска местоположения
    location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city}"
    location_response = requests.get(location_url)
    print(location_response)
    if location_response.status_code == 200:
        location_data = location_response.json()
        if location_data:
            return location_data[0]['Key']  # Возвращаем ключ местоположения
    return None

def translate(s, lng):
    return GT(source='auto', target=f'{lng}').translate(s)

def get_current_weather(location_key, location_key2):
    # URL для получения текущей погоды
    weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"
    weather_url2 = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key2}?apikey={api_key}"
    weather_response = requests.get(weather_url)
    weather_response2 = requests.get(weather_url2)
    if weather_response.status_code == 200 and weather_response2.status_code == 200:
        weather_data = weather_response.json()
        weather_data2 = weather_response2.json()
        return [weather_data[0], weather_data2[0]]  # Возвращаем данные о погоде
    return None


@app.route('/', methods=['GET', 'POST'])
def main():
    weather_info = None
    weather_info2 = None
    all_info = None
    if request.method == 'POST':
        city = translate(request.form['city'], 'en')
        city2 = translate(request.form['city2'], 'en')
        location_key = get_location_key(city)
        location_key2 = get_location_key(city2)
        if location_key and location_key2:
            all_info = get_current_weather(location_key, location_key2)
            weather_info = all_info[0]
            weather_info['LocalizedName'] = 'Пункт 1'
            weather_info2 = all_info[1]
            weather_info2['LocalizedName'] = 'Пункт 2'
            all_info = [weather_info, weather_info2]
            print(weather_info)
        else:
            all_info = {"error": "Не удалось найти местоположение."}

    return render_template('main_page.html', weather_info=all_info)


if __name__ == '__main__':
    app.run(debug=True)