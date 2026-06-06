#________________
# imports:

import httpx

#________________
# Base Setting:

API_KEY = "df119a38915d672fd0c7e3a635cd828f"

#________________
# Base:

def get_city_weather(city):
    try:

        BASE_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = httpx.get(BASE_URL)

        response.raise_for_status()

        data = response.json()

        temp = data['main']['temp']
        describtion = data['weather'][0]['description']
        humidity = data['main']['humidity'] 
        
        print(f"{city} weather status:\n")
        print(f"Tempeture: {temp}C")
        print(f"Describtion: {describtion}")
        print(f"Humidity: {humidity}")


    except httpx.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code}")

    except httpx.RequestError as e:
        print(f"❌ Network Error: {e}")

    except KeyError:
        print(f"❌ Error parsing the JSON data. Unexpected response format.")

city = "Ahvaz"

if __name__ == "__main__":
    get_city_weather(city=city)
    