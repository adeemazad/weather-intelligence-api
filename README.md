# Weather Intelligence API

A production-deployed REST API and visual weather dashboard providing real-time weather intelligence for cities worldwide.

Built with **Python**, **FastAPI**, **OpenWeatherMap API**, and deployed on **Railway**.

---

## Live API

**Base URL:**  
`https://weather-intelligence-api.up.railway.app`

**Visual Homepage:**  
`https://weather-intelligence-api.up.railway.app/`

**Interactive API Documentation:**  
`https://weather-intelligence-api.up.railway.app/docs`

**Example Visual Weather Page:**  
`https://weather-intelligence-api.up.railway.app/view/London`

---

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Visual API homepage |
| GET | `/view/{city}` | Visual weather page for a city |
| GET | `/weather/{city}` | JSON weather intelligence for a city |
| GET | `/compare?cities=A,B,C` | Compare weather across multiple cities |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API documentation |

---

## Example Requests

### Visual weather page

```text
GET /view/London
```

Example URL:

```text
https://weather-intelligence-api.up.railway.app/view/London
```

### JSON weather data

```text
GET /weather/London
```

Example URL:

```text
https://weather-intelligence-api.up.railway.app/weather/London
```

### Compare multiple cities

```text
GET /compare?cities=London,Paris,Tokyo
```

Example URL:

```text
https://weather-intelligence-api.up.railway.app/compare?cities=London,Paris,Tokyo
```

---

## Example JSON Response

**GET `/weather/London`**

```json
{
  "city": "London",
  "country": "GB",
  "timestamp": "2026-04-27T19:07:09.514868",
  "current_conditions": {
    "temperature_c": 17.9,
    "feels_like_c": 17,
    "heat_index_c": 26.3,
    "humidity_percent": 48,
    "pressure_hpa": 1022,
    "wind_speed_ms": 3.1,
    "visibility_m": 10000,
    "description": "overcast clouds",
    "icon": "04d"
  },
  "intelligence": {
    "risk_level": "LOW",
    "safety_recommendations": [
      "Conditions are comfortable for outdoor activity"
    ],
    "travel_advisory": "CLEAR — Good conditions for travel"
  }
}
```

---

## Features

- Real-time weather data for cities worldwide
- Visual homepage for easier navigation
- Visual city weather pages at `/view/{city}`
- JSON API endpoint at `/weather/{city}`
- Multi-city weather comparison endpoint
- Heat index calculation using the Rothfusz regression equation
- Safety risk assessment based on temperature, wind, and humidity
- Travel advisory based on visibility, wind speed, and weather conditions
- Interactive API documentation generated automatically by FastAPI

---

## Tech Stack

- **Python 3.11**
- **FastAPI** — modern, high-performance web framework
- **Uvicorn** — ASGI server
- **OpenWeatherMap API** — real-time weather data provider
- **Railway** — cloud deployment platform
- **GitHub** — version control and deployment source

---

## Run Locally

Clone the repository:

```bash
git clone https://github.com/adeemazad/weather-intelligence-api
```

Move into the project folder:

```bash
cd weather-intelligence-api
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project folder:

```text
OPENWEATHER_API_KEY=your_key_here
```

Run the API:

```bash
uvicorn main:app --reload
```

Open the local homepage:

```text
http://127.0.0.1:8000/
```

Open the local interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Project Structure

```text
weather-intelligence-api/
├── main.py
├── requirements.txt
├── Procfile
├── README.md
├── .gitignore
├── .env
└── venv/
```

---

## Environment Variables

The project requires one environment variable:

| Variable | Description |
|---|---|
| `OPENWEATHER_API_KEY` | API key from OpenWeatherMap |

The `.env` file is used locally and should not be uploaded to GitHub.

---

## Deployment

This project is deployed on Railway.

Railway uses the `Procfile` to start the API:

```text
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

The project is connected to GitHub, so updates pushed to the main branch can automatically redeploy the live API.

---

## Author

**Adeem Azad**  
BEng Mechatronics, University of Glasgow  

[LinkedIn](https://www.linkedin.com/in/adeem-azad)
