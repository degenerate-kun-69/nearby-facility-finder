# Nearby Facility finder
A python application that uses geoapify's free API to find nearby public facilities such as hospitals, police stations and schools. It also maintains a database and cache of everything fetched previously to reduce the API calls.

---

## Features
- Address Geocoding (text -> lat/lon)
- Facility dicovery within 2KM (adjustable)
- SQLite Caching for avoiding repeated API calls
- JSON logs for debugging
- Modular structure with clear seperation of concerns for easy debugging

---

## Tech Stack 
- **Python 3.13**
- **SQLite 3 (Python `sqlite3` package)**
- **Geoapify API**

---

## Setup
1. Clone and cd into the git repo with 
```bash
git clone https://github.com/degenerate-kun-69/nearby-facility-finder

cd nearby-facility-finder

```
2. Install requirements
```bash
pip install python-dotenv dotenv requests urllib3
```
3. Get a Geoapify key
- Register at [Geoapify](https://www.geoapify.com/)

4. Configure Environment
- Create a `.env` file in the root directory
```env
GEOAPIFY_API_KEY=<YOUR_API_KEY>
```
5. Run App
```bash
python3 main.py
``` 

---

## Project Structure
```graphql
.
├── api_handler.py        # Geoapify API interactions
├── db_handler.py         # SQLite DB logic (caching & storing)
├── location_finder.py    # Combines API and DB logic
├── config.py             # Loads the API key
├── main.py               # Entry point (CLI)
├── raw_cache/            # Stores JSON response files
├── facilities.db         # Generated SQLite DB
└── .env                  # API key (not committed)
```
---

## Logic Overview
1. User inputs address

2. App checks if data for this address/type is cached in DB

3. If not:
    - Geocodes address to coordinates
    - Fetches facilities from Geoapify
    - Stores facilities in DB
    - Saves raw JSON in raw_cache/

4. Displays all results (name, type, coordinates)

---

## Module overview
### `api_handler.py` - Geoapify API handler:
- Handles geocoding and nearby facility lookup
```Python
from urllib import request, parse
import json

class GeoapifyHandler:
    def geocode(self, address):
        url = f"https://api.geoapify.com/v1/geocode/search?text={parse.quote(address)}&apiKey=..."
        data = json.loads(request.urlopen(url).read())
        return data["features"][0]["geometry"]["coordinates"]  # lon, lat
```
- Gets nearby facilities
```python
    def get_nearby_facilities(self, lat, lon, types):
        url = f"https://api.geoapify.com/v2/places?...&filter=circle:{lon},{lat},2000"
        # returns names, types, addresses, coordinates
```
### `db_handler.py` - SQLite cache manager:
- Initializes DB tables and stores/retrieves data
```python
import sqlite3

class DBHandler:
    def create_tables(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS facilities (...)')
        self.conn.execute('CREATE TABLE IF NOT EXISTS location_cache (...)')
```
- Inserts and checks cache
```python
    def insert_facility(self, address, name, type_, lat, lon):
        self.conn.execute("INSERT INTO facilities VALUES (?, ?, ?, ?, ?)", ...)

    def is_cached(self, address, type_):
        cur = self.conn.execute("SELECT fetched FROM location_cache WHERE ...")
        return cur.fetchone() is not None
```
### `location_finder.py` — Core App Logic
- Controls the flow of address lookup, caching, and API calls
```python
class LocationFinder:
    def run(self, address):
        for place_type in ["hospital", "school", "police"]:
            if self.db.is_cached(address, place_type):
                facilities = self.db.get_cached_facilities(address, place_type)
            else:
                lat, lon = self.geo.geocode(address)
                results = self.geo.get_nearby_facilities(lat, lon, [place_type])
                self.db.insert_facility(...)
                self.db.cache_location(...)
```
- Also logs raw JSON
```python
    def save_json_debug(self, address, type_, data):
        with open("raw_cache/...json", "w") as f:
            json.dump(data, f)
```
### `config.py`- Load Secure API key
- Loads Geoapify key from .env using python-dotenv
```python
from dotenv import load_dotenv
load_dotenv()

import os
API_KEY = os.getenv("GEOAPIFY_API_KEY")
```
### `main.py` - CLI entry point
- Runs LocationFinder for user inputted address
```python
from location_finder import LocationFinder
from config import API_KEY

address = input("Enter your address: ")
finder = LocationFinder(API_KEY)
finder.run(address)
```

---

## Example output
```bash
Enter your address: Times Square, New York
[API CALL] Hospitals near Times Square, New York
[API CALL] Schools near Times Square, New York
[API CALL] Police near Times Square, New York
 - NY Presbyterian (hospital) @ (40.762, -73.984)
 - PS 35 School (school) @ (40.759, -73.985)
 - Midtown North Precinct (police) @ (40.761, -73.983)
```