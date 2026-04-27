from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI(
    title="Weather Intelligence API",
    description="""
    ## Real-time weather intelligence for any city worldwide.

    This API provides current weather conditions, heat index calculations,
    safety recommendations, travel advisories, and multi-city comparisons.

    ### Main Features
    - Real-time weather data
    - Heat index calculation
    - Safety risk assessment
    - Travel advisory generation
    - Multi-city weather comparison

    ### Example Requests
    - `/weather/London`
    - `/weather/Glasgow`
    - `/compare?cities=London,Paris,Tokyo`

    Built by Adeem Azad.
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


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Intelligence API</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: #ffffff;
            }

            .container {
                max-width: 950px;
                margin: 0 auto;
                padding: 50px 20px;
            }

            .card {
                background: rgba(255, 255, 255, 0.12);
                border-radius: 20px;
                padding: 35px;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
                backdrop-filter: blur(8px);
            }

            h1 {
                font-size: 42px;
                margin-bottom: 10px;
            }

            h2 {
                margin-top: 35px;
                color: #dbeafe;
            }

            p {
                font-size: 18px;
                line-height: 1.6;
            }

            .badge {
                display: inline-block;
                background: #22c55e;
                color: #052e16;
                padding: 8px 14px;
                border-radius: 999px;
                font-weight: bold;
                margin-bottom: 20px;
            }

            .endpoints {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }

            .endpoint {
                background: rgba(255, 255, 255, 0.14);
                padding: 18px;
                border-radius: 14px;
            }

            code {
                display: inline-block;
                background: rgba(0, 0, 0, 0.3);
                padding: 6px 8px;
                border-radius: 8px;
                color: #fef3c7;
            }

            a {
                color: #bfdbfe;
                font-weight: bold;
                text-decoration: none;
            }

            a:hover {
                text-decoration: underline;
            }

            .footer {
                margin-top: 35px;
                font-size: 14px;
                opacity: 0.85;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <span class="badge">Live API</span>

                <h1>Weather Intelligence API</h1>

                <p>
                    A real-time weather intelligence API that provides current weather,
                    safety recommendations, heat index calculations, and travel advisories
                    for cities worldwide.
                </p>

                <h2>Available Endpoints</h2>

                <div class="endpoints">
                    <div class="endpoint">
                        <strong>API Homepage</strong><br>
                        <code>GET /</code>
                    </div>

                    <div class="endpoint">
                        <strong>Weather by City</strong><br>
                        <code>GET /weather/London</code>
                    </div>

                    <div class="endpoint">
                        <strong>Compare Cities</strong><br>
                        <code>GET /compare?cities=London,Paris,Tokyo</code>
                    </div>

                    <div class="endpoint">
                        <strong>Health Check</strong><br>
                        <code>GET /health</code>
                    </div>

                    <div class="endpoint">
                        <strong>Interactive Docs</strong><br>
                        <code>GET /docs</code>
                    </div>
                </div>

                <h2>Try It Now</h2>

                <p>
                    <a href="/weather/London">Check London Weather</a><br>
                    <a href="/compare?cities=London,Paris,Tokyo">Compare London, Paris, and Tokyo</a><br>
                    <a href="/docs">Open Interactive API Docs</a>
                </p>

                <h2>Built With</h2>

                <p>
                    Python, FastAPI, OpenWeatherMap API, and Railway.
                </p>

                <div class="footer">
                    Built by Adeem Azad | Version 1.0.0
                </div>
            </div>
        </div>
    </body>
    </html>
    """


@app.get(
    "/health",
    summary="Health check",
    description="Checks whether the API is running successfully."
)
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get(
    "/weather/{city}",
    summary="Get weather intelligence for a city",
    description="Returns real-time weather data, heat index, safety recommendations, and travel advisory for a given city."
)
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


@app.get(
    "/compare",
    summary="Compare weather across multiple cities",
    description="Compares weather conditions for 2 to 5 cities and sorts them by temperature."
)
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
@app.get("/view/{city}", response_class=HTMLResponse)
def view_weather(city: str):
    weather = get_weather(city)

    conditions = weather["current_conditions"]
    intelligence = weather["intelligence"]

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather in {weather["city"]}</title>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #0f172a, #2563eb);
                color: white;
            }}

            .container {{
                max-width: 900px;
                margin: 0 auto;
                padding: 50px 20px;
            }}

            .card {{
                background: rgba(255, 255, 255, 0.12);
                border-radius: 22px;
                padding: 35px;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(8px);
            }}

            h1 {{
                font-size: 42px;
                margin-bottom: 5px;
            }}

            .temperature {{
                font-size: 70px;
                font-weight: bold;
                margin: 25px 0 5px;
            }}

            .description {{
                font-size: 24px;
                text-transform: capitalize;
                opacity: 0.9;
            }}

            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 15px;
                margin-top: 30px;
            }}

            .box {{
                background: rgba(255, 255, 255, 0.14);
                padding: 18px;
                border-radius: 16px;
            }}

            .label {{
                font-size: 14px;
                opacity: 0.75;
            }}

            .value {{
                font-size: 22px;
                font-weight: bold;
                margin-top: 6px;
            }}

            .risk {{
                display: inline-block;
                margin-top: 25px;
                padding: 10px 16px;
                border-radius: 999px;
                background: #22c55e;
                color: #052e16;
                font-weight: bold;
            }}

            ul {{
                line-height: 1.8;
            }}

            a {{
                color: #bfdbfe;
                font-weight: bold;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}

            .footer {{
                margin-top: 30px;
                opacity: 0.85;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <div class="card">
                <h1>{weather["city"]}, {weather["country"]}</h1>
                <div class="description">{conditions["description"]}</div>

                <div class="temperature">{conditions["temperature_c"]}°C</div>
                <div>Feels like {conditions["feels_like_c"]}°C</div>

                <div class="risk">Risk Level: {intelligence["risk_level"]}</div>

                <div class="grid">
                    <div class="box">
                        <div class="label">Humidity</div>
                        <div class="value">{conditions["humidity_percent"]}%</div>
                    </div>

                    <div class="box">
                        <div class="label">Wind Speed</div>
                        <div class="value">{conditions["wind_speed_ms"]} m/s</div>
                    </div>

                    <div class="box">
                        <div class="label">Pressure</div>
                        <div class="value">{conditions["pressure_hpa"]} hPa</div>
                    </div>

                    <div class="box">
                        <div class="label">Visibility</div>
                        <div class="value">{conditions["visibility_m"]} m</div>
                    </div>

                    <div class="box">
                        <div class="label">Heat Index</div>
                        <div class="value">{conditions["heat_index_c"]}°C</div>
                    </div>

                    <div class="box">
                        <div class="label">Travel Advisory</div>
                        <div class="value">{intelligence["travel_advisory"]}</div>
                    </div>
                </div>

                <h2>Safety Recommendations</h2>
                <ul>
                    {"".join([f"<li>{item}</li>" for item in intelligence["safety_recommendations"]])}
                </ul>

                <div class="footer">
                    <a href="/">Back to homepage</a> |
                    <a href="/weather/{city}">View raw JSON</a> |
                    <a href="/docs">API docs</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """