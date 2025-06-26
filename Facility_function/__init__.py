# main.py
from location_finder import LocationFinder
from config import API_KEY

if __name__ == "__main__":
    address = input("Enter your address: ")
    finder = LocationFinder(API_KEY)
    finder.run(address)