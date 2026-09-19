# Weather ETL Pipeline

Sebuah aplikasi ETL sederhana yang mengambil data cuaca real-time dari Open-Meteo untuk lokasi Jakarta, lalu membersihkannya dan menyimpannya ke database SQLite.

## Deskripsi

Project ini dibuat untuk menunjukkan alur dasar Extract-Transform-Load (ETL) menggunakan Python. Aplikasi ini akan:

- mengambil data cuaca terkini dari API Open-Meteo,
- memproses dan membersihkan data agar siap dipakai,
- menyimpan hasilnya ke tabel SQLite bernama `daily_weather`.

## Fitur

- Mengambil data cuaca dari API Open-Meteo tanpa memerlukan API key
- Menggunakan koordinat Jakarta: latitude `-6.2146` dan longitude `106.8451`
- Menyimpan data ke SQLite database
- Mencatat timestamp, kota, suhu, kelembaban, dan deskripsi cuaca
- Mudah dijalankan dan dikembangkan untuk kebutuhan ETL lanjutan

## Teknologi yang Digunakan

- Python 3
- `requests` untuk mengakses API
- `sqlite3` untuk database lokal
- Open-Meteo API sebagai sumber data

## Struktur Proyek

```text
weather-etl-pipeline/
├── etl_weather.py
├── weather_data.db
├── README.md
└── .gitignore
```

## Cara Kerja

Aplikasi ini terdiri dari 3 tahapan utama:

1. Extract
   - Mengambil data cuaca dari endpoint Open-Meteo.
   - Data yang diambil berisi suhu saat ini, kelembaban, dan `weather_code`.

2. Transform
   - Mengambil field yang diperlukan dari response JSON.
   - Menyusun data ke format yang rapi sebelum disimpan.

3. Load
   - Membuat tabel `daily_weather` jika belum ada.
   - Menyimpan data ke SQLite database.

## Prasyarat

Pastikan perangkat Anda sudah memiliki:

- Python 3.x
- koneksi internet untuk mengakses API Open-Meteo
- paket Python `requests`

## Instalasi

1. Clone repository:

```bash
git clone <url-repository>
cd weather-etl-pipeline
```

2. Instal dependency:

```bash
pip install requests
```

## Menjalankan Aplikasi

Jalankan perintah berikut di root project:

```bash
python etl_weather.py
```

Setelah dijalankan, aplikasi akan otomatis:

- mengambil data cuaca terbaru,
- memproses data,
- menyimpan hasil ke file `weather_data.db`.

## Skema Database

Tabel yang dibuat bernama `daily_weather` dengan struktur berikut:

```sql
CREATE TABLE daily_weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    city TEXT,
    temperature REAL,
    humidity INTEGER,
    description TEXT
);
```

## Contoh Query SQLite

Untuk melihat data yang sudah tersimpan:

```bash
sqlite3 weather_data.db "SELECT * FROM daily_weather;"
```

Atau melalui Python:

```python
import sqlite3

conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM daily_weather')
rows = cursor.fetchall()
print(rows)
conn.close()
```

## Catatan

- Koordinat lokasi saat ini diatur tetap ke Jakarta.
- `description` diisi dari `weather_code` yang dikonversi ke string.
- Data akan ditambah setiap kali script dijalankan.

## Lisensi

Project ini bersifat open untuk kebutuhan pembelajaran dan pengembangan lebih lanjut.
