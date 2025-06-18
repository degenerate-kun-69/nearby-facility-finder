# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")
print("Loaded API KEY:", API_KEY)

if not API_KEY:
    raise ValueError("Missing GEOAPIFY_API_KEY in .env file")