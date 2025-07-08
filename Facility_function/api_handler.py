# api_handler.py
import urllib.request
import urllib.parse
import json

class GeoapifyHandler:
    def __init__(self, api_key): #initialize with API key referenced in location_finder.py
        self.api_key = api_key

    def geocode(self, address):
        url = f"https://api.geoapify.com/v1/geocode/search?text={urllib.parse.quote(address)}&apiKey={self.api_key}" #api call according to geoapify
        print("[DEBUG] Request URL:", url) #debug line to check req url
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read()) #read response and parse as JSON
            coords = data["features"][0]["geometry"]["coordinates"]
            return coords[1], coords[0]  # lat, lon return 

    def get_nearby_facilities(self, lat, lon, types):
        category_map={ #dict to map types to geoapify categories
            "hospital": "healthcare.hospital",
            "school": "education.school",
            "police": "service.police"
        }
        all_facilities = []#accumulator for all facilities found
        for type_ in types: #iterate over types
            category=category_map.get(type_)
            if not category:
                print(f"[ERROR] Unsupported type: {type_}")
                continue
            url = f"https://api.geoapify.com/v2/places?categories={category}&filter=circle:{lon},{lat},2000&limit=5&apiKey={self.api_key}" #2km radius search with places api call and max 5 results
            with urllib.request.urlopen(url) as response: 
                data = json.loads(response.read()) #parse json and make api req
                for f in data["features"]: #data extractor
                    props = f["properties"]
                    all_facilities.append({
                        "name": props.get("name", "Unknown"),
                        "type": type_,
                        "address": props.get("formatted", "No address"),
                        "lat": f["geometry"]["coordinates"][1],
                        "lon": f["geometry"]["coordinates"][0]
                    })
        return all_facilities #returm ;ost of facility dict
