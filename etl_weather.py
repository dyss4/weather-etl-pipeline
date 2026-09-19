import logging
import sqlite3
from datetime import datetime

import requests

# Koordinat Jakarta
LAT = -6.2146
LON = 106.8451
DB_NAME = "weather_data.db"
API_URL = "https://api.open-meteo.com/v1/forecast"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def weather_code_to_description(code: int) -> str:
    #Mengubah weather_code Open-Meteo menjadi teks yang lebih mudah dibaca."""
    weather_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return weather_map.get(code, "Unknown weather condition")


def extract_data(lat: float = LAT, lon: float = LON):
    #Mengambil data cuaca terkini dari Open-Meteo."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code",
    }

    try:
        logger.info("Memulai extract data cuaca dari Open-Meteo...")
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        logger.info("Data cuaca berhasil diambil.")
        return data
    except requests.exceptions.Timeout:
        logger.error("Request ke Open-Meteo timeout.")
        return None
    except requests.exceptions.RequestException as exc:
        logger.exception("Error saat mengambil data cuaca: %s", exc)
        return None


def transform_data(raw_data):
    #Membersihkan dan memformat data mentah dari API."""
    if not raw_data:
        logger.warning("Tidak ada data mentah untuk ditransform.")
        return None

    try:
        logger.info("Memulai transform data...")
        current = raw_data["current"]
        timestamp = current.get("time", datetime.now().isoformat())
        city = "Jakarta"
        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        weather_code = int(current["weather_code"])
        description = weather_code_to_description(weather_code)
        logger.info("Data berhasil ditransform: %s", {
            "weather_code": weather_code,
            "description": description
        })
        return {
            "timestamp": timestamp,
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "weather_code": weather_code,
            "description": description,
        }
    except (KeyError, TypeError, ValueError) as exc:
        logger.exception("Error saat transform data: %s", exc)
        return None


def load_data(clean_data):
    """Menyimpan data bersih ke database SQLite."""
    if not clean_data:
        logger.warning("Tidak ada data untuk dimuat ke database.")
        return

    try:
        logger.info("Memulai load data ke database...")
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    city TEXT,
                    temperature REAL,
                    humidity INTEGER,
                    description TEXT
                )
                """
            )

            conn.execute(
                """
                INSERT INTO daily_weather (timestamp, city, temperature, humidity, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    clean_data["timestamp"],
                    clean_data["city"],
                    clean_data["temperature"],
                    clean_data["humidity"],
                    clean_data["description"],
                ),
            )
            conn.commit()

        logger.info("Data berhasil disimpan: %s", clean_data)
    except sqlite3.Error as exc:
        logger.exception("Error database: %s", exc)


def main():
    raw_data = extract_data()
    clean_data = transform_data(raw_data)
    load_data(clean_data)


if __name__ == "__main__":
    main()

