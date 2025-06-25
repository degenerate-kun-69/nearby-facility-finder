# db_handler.py
import sqlite3
import json

class DBHandler:
    def __init__(self, db_name="facilities.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS facilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT,
                name TEXT,
                type TEXT,
                lat REAL,
                lon REAL
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS location_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT,
                type TEXT,
                fetched BOOLEAN,
                lat REAL,
                lon REAL,
                raw_json TEXT
            )
        ''')
        self.conn.commit()

    def insert_facility(self, address, name, type_, lat, lon):
        self.conn.execute('''
            INSERT INTO facilities (address, name, type, lat, lon)
            VALUES (?, ?, ?, ?, ?)
        ''', (address, name, type_, lat, lon))
        self.conn.commit()

    def get_cached_facilities(self, address, type_):
        cur = self.conn.execute('''
            SELECT name, type, lat, lon FROM facilities
            WHERE address = ? AND type = ?
        ''', (address, type_))
        return cur.fetchall()

    def is_cached(self, address, type_):
        cur = self.conn.execute('''
            SELECT fetched FROM location_cache WHERE address = ? AND type = ?
        ''', (address, type_))
        return cur.fetchone() is not None

    def cache_location(self, address, type_, lat, lon, raw_json):
        self.conn.execute('''
            INSERT INTO location_cache (address, type, fetched, lat, lon, raw_json)
            VALUES (?, ?, 1, ?, ?, ?)
        ''', (address, type_, lat, lon, json.dumps(raw_json)))
        self.conn.commit()
