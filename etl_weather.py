import requests
import sqlite3
from datetime import datetime

# Koordinat Jakarta
LAT = -6.2146
LON = 106.8451

def extract_data():
    #EXTRACT: Mengambil data dari Open-Meteo (Tanpa API Key)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,weather_code"
    try:
        print(f"[{datetime.now()}] Memulai Extract data dari Open-Meteo...")
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error saat Extract data: {e}")
        return None

def transform_data(raw_data):
    #TRANSFORM: Membersihkan JSON dari Open-Meteo
    if not raw_data:
        return None
    
    try:
        print(f"[{datetime.now()}] Memulai Transform data...")
        current = raw_data['current']
        
        temp = current['temperature_2m']
        humidity = current['relative_humidity_2m']
        weather_code = str(current['weather_code']) # Open-Meteo menggunakan kode angka untuk cuaca
        timestamp = current['time']
        city = "Jakarta"
        
        # Format sesuai dengan fungsi load_data sebelumnya
        clean_data = (timestamp, city, temp, humidity, weather_code)
        return clean_data
    except KeyError as e:
        print(f"Error saat Transform data: {e}")
        return None

# Fungsi load_data() tetap sama persis seperti sebelumnya
