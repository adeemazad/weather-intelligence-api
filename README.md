# Weather Intelligence API

A production-deployed REST API providing real-time weather intelligence 
for any city worldwide. Built with Python and FastAPI, containerised 
with Docker, and deployed on Railway.

## Live API

**Base URL:** `https://weather-intelligence-api.up.railway.app/weather/{city}`

| Endpoint | Description |
|---|---|
| `GET /` | API info and available endpoints |
| `GET /weather/{city}` | Full weather intelligence for a city |
| `GET /compare?cities=A,B,C` | Compare weather across multiple cities |
| `GET /health` | Health check |
| `GET /docs` | Interactive API documentation |

## Example Responses

**GET /weather/London**
```json
{
  "city": "London",
  "country": "GB",
  "current_conditions": {
    "temperature_c": 14.2,
    "humidity_percent": 72,
    "wind_speed_ms": 5.1,
    "description": "light rain"
  },
  "intelligence": {
    "risk_level": "LOW",
    "safety_recommendations": ["Conditions comfortable for outdoor activity"],
    "travel_advisory": "CAUTION — Precipitation may affect driving"
  }
}
```

## Features

- Real-time weather data for any city worldwide
- Heat index calculation using Rothfusz regression equation
- Safety risk assessment based on temperature, wind, and humidity
- Travel advisory based on visibility and weather conditions
- Multi-city comparison endpoint
- Auto-generated interactive API documentation at /docs

## Tech Stack

- **Python 3.11**
- **FastAPI** — modern, high-performance web framework
- **Uvicorn** — ASGI server
- **OpenWeatherMap API** — real-time weather data
- **Railway** — cloud deployment platform

## Run Locally

```bash
git clone https://github.com/adeemazad/weather-intelligence-api
cd weather-intelligence-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
OPENWEATHER_API_KEY=your_key_here

Run:
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for interactive documentation.

## Author

**Adeem Azad**
BEng Mechatronics, University of Glasgow
[LinkedIn](https://www.linkedin.com/in/adeem-azad)
