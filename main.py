#________________
# imports:

from fastapi import FastAPI, HTTPException, Query
import httpx
import asyncio

#________________
# Base Setting:

app = FastAPI(title="Farbod Weather API", description="Using api to find any city weather data!")

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
        
        return {
            "city": city.capitalize(),
            "temp": data['main']['temp'],
            "describtion": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "status": "success"
        }


    except httpx.HTTPError as e:
        return {"city": city, "status": "failed", "error": "City not found or invalid API key."}

    except httpx.RequestError as e:
        return {"city": city, "status": "failed", "error": "Network connection error."}


#_______________________
# Run App:

@app.get("/weather/{city}")
async def get_single_city_weather(city: str):
    async with httpx.AsyncClient() as client:
        result = await fetch_weather(client, city)
        if result["status"] == "failed":
            raise HTTPException(status_code=404, detail=result["error"])
        return result

@app.get("/weather/bulk/")
async def get_bulk_weather(cities: str = Query(..., description="Enter cities name by comma ','")):
    city_list = [c.strip() for c in cities.split(",")]

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_weather(client, city) for city in city_list]
        results = await asyncio.gather(*tasks)

    return {"total_cities": len(city_list), "data": results}