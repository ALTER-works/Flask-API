import requests
from deep_translator import GoogleTranslator as GT
from flask import Flask, render_template, request

app = Flask(__name__)

api_key = "G6K81pyXN2A1tDA5HFV8SUr5sdbarQ24"

def translate(s, lng):
    return GT(source='auto', target=f'{lng}').translate(s)


def get_location_key(city):
    location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city}"
    location_response = requests.get(location_url)
    if location_response.status_code == 200:
        location_data = location_response.json()
        if location_data:
            return {
                'Key': location_data[0]['Key'],
                'Latitude': location_data[0]['GeoPosition']['Latitude'],
                'Longitude': location_data[0]['GeoPosition']['Longitude']
            }
    return None


def get_current_weather(location_key, location_key2):
    weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"
    weather_url2 = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key2}?apikey={api_key}"

    weather_response = requests.get(weather_url)
    weather_response2 = requests.get(weather_url2)

    if weather_response.status_code == 200 and weather_response2.status_code == 200:
        return [weather_response.json()[0], weather_response2.json()[0]]  # Return both sets of data
    return None


@app.route('/', methods=['GET', 'POST'])
def main():
    all_info = None
    if request.method == 'POST':
        city = translate(request.form['city'], 'en')
        city2 = translate(request.form['city2'], 'en')

        location_data = get_location_key(city)
        location_data2 = get_location_key(city2)

        if location_data and location_data2:
            all_info = get_current_weather(location_data['Key'], location_data2['Key'])

            all_info[0].update(
                {'GeoPosition': {'Latitude': location_data['Latitude'], 'Longitude': location_data['Longitude']}})
            all_info[1].update(
                {'GeoPosition': {'Latitude': location_data2['Latitude'], 'Longitude': location_data2['Longitude']}})

            all_info[0]['LocalizedName'] = translate(request.form['city'], 'ru')
            if all_info[0]['WeatherText'] == 'Clear': all_info[0]['WeatherText'] = 'Ясно'
            else: all_info[0]['WeatherText'] = translate(all_info[0]['WeatherText'], 'ru')

            all_info[1]['LocalizedName'] = translate(request.form['city2'], 'ru')
            if all_info[1]['WeatherText'] == 'Clear': all_info[1]['WeatherText'] = 'Ясно'
            else: all_info[1]['WeatherText'] = translate(all_info[1]['WeatherText'], 'ru')

        else:
            all_info = {"error": "Не удалось найти местоположение."}

    return render_template('main_page.html', weather_info=all_info)


if __name__ == '__main__':
    app.run(debug=True)
