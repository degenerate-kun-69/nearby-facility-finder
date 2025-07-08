# location_finder.py
from Facility_function.api_handler import GeoapifyHandler
from Facility_function.db_handler import DBHandler

class LocationFinder:
    def __init__(self, api_key):
        self.geo = GeoapifyHandler(api_key) #init geoapify handler with api key
        self.db = DBHandler() #init cosmos db handler

    def run(self, address):
        output = []
        types = ["hospital", "school", "police"]

        for place_type in types:
            if self.db.is_cached(address, place_type): #check if data is cached
                output.append(f"{place_type.title()}s near {address}")
                print(f"[CACHE HIT] {place_type.title()}s near {address}") #terminal output for cache hit in azure portal
                facilities = self.db.get_cached_facilities(address, place_type)
            else:
                output.append(f"{place_type.title()}s near {address}")
                print(f"[API CALL] {place_type.title()}s near {address}") #terminal output for api call in azure portal
                lat, lon = self.geo.geocode(address) #geocode
                results = self.geo.get_nearby_facilities(lat, lon, [place_type]) #call api with lat long and place type
                for f in results: #store in db to reduce api calls
                    self.db.insert_facility(address, f["name"], f["type"], f["lat"], f["lon"])
                self.db.cache_location(address, place_type, lat, lon, results)
                facilities = self.db.get_cached_facilities(address, place_type)

            for f in facilities: #output formatting in form "Name (Type) @ (Lat, Lon)"
                output.append(f" - {f[0]} ({f[1]}) @ ({f[2]}, {f[3]})")
                print(f" - {f[0]} ({f[1]}) @ ({f[2]}, {f[3]})")
        return "\n".join(output)
