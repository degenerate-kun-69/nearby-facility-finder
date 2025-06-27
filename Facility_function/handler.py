# handler.py
from Facility_function.location_finder import LocationFinder
from Facility_function.config import API_KEY

def handle_facility_request(address: str) -> str:
    finder = LocationFinder(API_KEY)
    result = finder.run(address)
    return result
