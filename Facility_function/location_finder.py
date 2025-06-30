# location_finder.py
from Facility_function.api_handler import GeoapifyHandler
from Facility_function.db_handler import DBHandler
import json
import os
import time

class LocationFinder:
    def __init__(self, api_key):
        self.geo = GeoapifyHandler(api_key)
        self.db = DBHandler()

    def run(self, address):
        output = []
        types = ["hospital", "school", "police"]

        for place_type in types:
            if self.db.is_cached(address, place_type):
                output.append(f"{place_type.title()}s near {address}")
                print(f"[CACHE HIT] {place_type.title()}s near {address}")
                facilities = self.db.get_cached_facilities(address, place_type)
            else:
                output.append(f"{place_type.title()}s near {address}")
                print(f"[API CALL] {place_type.title()}s near {address}")
                lat, lon = self.geo.geocode(address)
                results = self.geo.get_nearby_facilities(lat, lon, [place_type])
                for f in results:
                    self.db.insert_facility(address, f["name"], f["type"], f["lat"], f["lon"])
                self.db.cache_location(address, place_type, lat, lon, results)
                #self.save_json_debug(address, place_type, results)
                #time.sleep(20.0) # Simulate delay for cache to be available
                facilities = self.db.get_cached_facilities(address, place_type)

            for f in facilities:
                output.append(f" - {f[0]} ({f[1]}) @ ({f[2]}, {f[3]})")
                print(f" - {f[0]} ({f[1]}) @ ({f[2]}, {f[3]})")
        return "\n".join(output)
'''
def save_json_debug(self, address, type_, data):
    os.makedirs("raw_cache", exist_ok=True)
    filename = f"raw_cache/{address.replace(' ', '_')}_{type_}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)'''