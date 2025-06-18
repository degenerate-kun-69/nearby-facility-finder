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