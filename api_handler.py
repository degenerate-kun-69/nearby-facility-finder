# api_handler.py
import urllib.request
import urllib.parse
import json

class GeoapifyHandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def geocode(self, address):
        url = f"https://api.geoapify.com/v1/geocode/search?text={urllib.parse.quote(address)}&apiKey={self.api_key}"
        print("[DEBUG] Request URL:", url)
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            coords = data["features"][0]["geometry"]["coordinates"]
            return coords[1], coords[0]  # lat, lon

    def get_nearby_facilities(self, lat, lon, types):
        category_map={
            "hospital": "healthcare.hospital",
            "school": "education.school",
            "police": "service.police"
        }
        all_facilities = []
        for type_ in types:
            category=category_map.get(type_)
            if not category:
                print(f"[ERROR] Unsupported type: {type_}")
                continue
            url = f"https://api.geoapify.com/v2/places?categories={category}&filter=circle:{lon},{lat},2000&limit=5&apiKey={self.api_key}" #for hospitals, need healthcare.hospital
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                for f in data["features"]:
                    props = f["properties"]
                    all_facilities.append({
                        "name": props.get("name", "Unknown"),
                        "type": type_,
                        "address": props.get("formatted", "No address"),
                        "lat": f["geometry"]["coordinates"][1],
                        "lon": f["geometry"]["coordinates"][0]
                    })
        return all_facilities
