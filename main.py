#________________
# imports:

import httpx
import asyncio
import time

#________________
# Base Setting:

API_KEY = "df119a38915d672fd0c7e3a635cd828f"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

#________________
# Base:

async def fetch_weather(client, city):
    params = {
        "q":city,
        "appid":API_KEY,
        "units":"metrics" 
    }

    try:

        response = await client.get(BASE_URL, params=params)

        response.raise_for_status()

        data = response.json()

        temp = data['main']['temp']
        describtion = data['weather'][0]['description']
        humidity = data['main']['humidity'] 
        
        print(f"{city} weather status:\n")
        print(f"Tempeture: {temp}C")
        print(f"Describtion: {describtion}")
        print(f"Humidity: {humidity}")
        print(f"_"*10, end='\n')


    except httpx.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code}")

    except httpx.RequestError as e:
        print(f"❌ Network Error: {e}")

    except KeyError:
        print(f"❌ Error parsing the JSON data. Unexpected response format.")

async def main():
    cities = ["Ahvaz", "Tehran", "London", "Tokyo", "New York", "Paris"]

    print("🚀 Fetching weather data concurrently...\n")
    start = time.time()

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_weather(client, city) for city in cities]

        await asyncio.gather(*tasks)

    end = time.time()
    print(f"\n⏱️ Total time taken: {end - start:.2f} seconds")

if __name__ == "__main__":

    asyncio.run(main())
