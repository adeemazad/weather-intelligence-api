from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI(
    title="Weather Intelligence API",
    description="""
    A real-time weather intelligence API that provides weather data,
    heat index calculations, safety recommendations, and travel advisories
    for any city worldwide.
    
    Built by Adeem Azad — github.com/adeemazad
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5"


def calculate_heat_index(temp_c: float, humidity: float) -> float:
    """Calculate heat index using Rothfusz regression equation."""
    t = (temp_c * 9/5) + 32  # Convert to Fahrenheit
    hi = (-42.379 + 2.04901523*t + 10.14333127*humidity
          - 0.22475541*t*humidity - 0.00683783*t*t
          - 0.05481717*humidity*humidity + 0.00122874*t*t*humidity
          + 0.00085282*t*humidity*humidity
          - 0.00000199*t*t*humidity*humidity)
    return round((hi - 32) * 5/9, 1)  # Convert back to Celsius


def get_safety_recommendation(temp_c: float, 
                               wind_speed: float, 
                               humidity: float) -> dict:
    """Generate safety recommendations based on weather conditions."""
    recommendations = []
    risk_level = "LOW"

    if temp_c > 35:
        recommendations.append("Extreme heat — avoid outdoor activity")
        risk_level = "HIGH"
    elif temp_c > 28:
        recommendations.append("High temperature — stay hydrated")
        risk_level = "MEDIUM"
    elif temp_c < 0:
        recommendations.append("Freezing conditions — dress in layers")
        risk_level = "MEDIUM"
    elif temp_c < -10:
        recommendations.append("Extreme cold — limit time outdoors")
        risk_level = "HIGH"

    if wind_speed > 20:
        recommendations.append("Strong winds — secure loose objects")
        risk_level = "HIGH"
    elif wind_speed > 10:
        recommendations.append("Moderate winds — caution outdoors")

    if humidity > 85:
        recommendations.append("Very high humidity — heat exhaustion risk")

    if not recommendations:
        recommendations.append("Conditions are comfortable for outdoor activity")

    return {
        "risk_level": risk_level,
        "recommendations": recommendations
    }


def get_travel_advisory(visibility: float, 
                         wind_speed: float, 
                         weather_id: int) -> str:
    """Generate travel advisory based on weather conditions."""
    if visibility < 1000:
        return "AVOID TRAVEL — Very low visibility"
    if wind_speed > 25:
        return "AVOID TRAVEL — Dangerous wind speeds"
    if weather_id in range(200, 300):
        return "CAUTION — Thunderstorms in area"
    if weather_id in range(300, 600):
        return "CAUTION — Precipitation may affect driving"
    if weather_id in range(600, 700):
        return "CAUTION — Snow or ice on roads possible"
    if weather_id in range(700, 800):
        return "CAUTION — Reduced visibility conditions"
    return "CLEAR — Good conditions for travel"


@app.get("/")
def root():
    return {
        "message": "Weather Intelligence API",
        "version": "1.0.0",
        "author": "Adeem Azad",
        "github": "github.com/adeemazad",
        "endpoints": {
            "weather": "/weather/{city}",
            "compare": "/compare?cities=London,Paris,Tokyo",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/weather/{city}")
def get_weather(city: str):
    """
    Get comprehensive weather intelligence for any city.
    
    Returns current conditions, heat index, safety recommendations,
    and travel advisory.
    """
    if not API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="API key not configured"
        )

    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found"
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Weather service unavailable"
        )

    data = response.json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    visibility = data.get("visibility", 10000)
    weather_id = data["weather"][0]["id"]

    heat_index = calculate_heat_index(temp, humidity)
    safety = get_safety_recommendation(temp, wind_speed, humidity)
    travel = get_travel_advisory(visibility, wind_speed, weather_id)

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "timestamp": datetime.utcnow().isoformat(),
        "current_conditions": {
            "temperature_c": round(temp, 1),
            "feels_like_c": round(data["main"]["feels_like"], 1),
            "heat_index_c": heat_index,
            "humidity_percent": humidity,
            "pressure_hpa": data["main"]["pressure"],
            "wind_speed_ms": round(wind_speed, 1),
            "visibility_m": visibility,
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        },
        "intelligence": {
            "risk_level": safety["risk_level"],
            "safety_recommendations": safety["recommendations"],
            "travel_advisory": travel
        }
    }


@app.get("/compare")
def compare_cities(cities: str):
    """
    Compare weather conditions across multiple cities.
    
    Usage: /compare?cities=London,Paris,Tokyo
    """
    city_list = [c.strip() for c in cities.split(",")]

    if len(city_list) < 2:
        raise HTTPException(
            status_code=400,
            detail="Please provide at least 2 cities separated by commas"
        )

    if len(city_list) > 5:
        raise HTTPException(
            status_code=400,
            detail="Maximum 5 cities per comparison"
        )

    results = []
    for city in city_list:
        try:
            weather = get_weather(city)
            results.append({
                "city": weather["city"],
                "country": weather["country"],
                "temperature_c": weather["current_conditions"]["temperature_c"],
                "humidity_percent": weather["current_conditions"]["humidity_percent"],
                "description": weather["current_conditions"]["description"],
                "risk_level": weather["intelligence"]["risk_level"],
                "travel_advisory": weather["intelligence"]["travel_advisory"]
            })
        except HTTPException as e:
            results.append({
                "city": city,
                "error": e.detail
            })

    results.sort(key=lambda x: x.get("temperature_c", -999), reverse=True)

    return {
        "comparison": results,
        "warmest": results[0].get("city") if results else None,
        "coolest": results[-1].get("city") if results else None,
        "timestamp": datetime.utcnow().isoformat()
    }