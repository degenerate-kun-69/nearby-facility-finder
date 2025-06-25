# main.py
from Facility_function.location_finder import LocationFinder
from Facility_function.config import API_KEY

if __name__ == "__main__":
    address = input("Enter your address: ")
    finder = LocationFinder(API_KEY)
    finder.run(address)