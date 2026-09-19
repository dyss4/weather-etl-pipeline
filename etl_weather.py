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
        weather_code = str(current['weather_code'])
        timestamp = current['time']
        city = "Jakarta"
        
        clean_data = (timestamp, city, temp, humidity, weather_code)
        return clean_data
    except KeyError as e:
        print(f"Error saat Transform data: {e}")
        return None

def load_data(clean_data):
    #LOAD: Menyimpan data bersih ke database SQLite
    if not clean_data:
        print("Tidak ada data untuk di-load.")
        return
    try:
        print(f"[{datetime.now()}] Memulai Load data ke database...")
        conn = sqlite3.connect('weather_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                city TEXT,
                temperature REAL,
                humidity INTEGER,
                description TEXT
            )
        ''')
        
        cursor.execute('''
            INSERT INTO daily_weather (timestamp, city, temperature, humidity, description)
            VALUES (?, ?, ?, ?, ?)
        ''', clean_data)
        
        conn.commit()
        print(f"[{datetime.now()}] Berhasil menyimpan data: {clean_data}")
    except sqlite3.Error as e:
        print(f"Error database: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

# INI ADALAH BLOK PEMICUNYA (Jangan sampai terhapus)
if __name__ == "__main__":
    raw = extract_data()
    clean = transform_data(raw)
    load_data(clean)

#for testing, you can run the following command in your terminal to view the data in the SQLite database:
#sqlite3 weather_data.db "SELECT * FROM daily_weather;"
