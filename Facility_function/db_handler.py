import os
import json
import uuid
from azure.cosmos import CosmosClient, PartitionKey

class DBHandler:
    def __init__(self):
        # Read Cosmos DB connection settings from environment variables
        self.endpoint = os.getenv("COSMOS_URI")
        self.key = os.getenv("COSMOS_KEY")

        if not self.endpoint or not self.key:
            raise ValueError("Missing COSMOS_URI or COSMOS_KEY environment variables")

        # Initialize the Cosmos DB client
        self.client = CosmosClient(self.endpoint, self.key)

        # Define database and container names
        self.database_name = "NearbyFacilitiesDB"
        self.facility_container_name = "Facilities"
        self.cache_container_name = "LocationCache"

        # Ensure the database and containers exist
        self._setup_db()

    def _setup_db(self):
        # Create the database if it doesn't already exist
        self.database = self.client.create_database_if_not_exists(self.database_name)

        # Create the facilities container with /address as partition key
        self.facility_container = self.database.create_container_if_not_exists(
            id=self.facility_container_name,
            partition_key=PartitionKey(path="/address"),
            offer_throughput=400
        )

        # Create the cache container with /address as partition key
        self.cache_container = self.database.create_container_if_not_exists(
            id=self.cache_container_name,
            partition_key=PartitionKey(path="/address"),
            offer_throughput=400
        )

    def insert_facility(self, address, name, type_, lat, lon):
        
        #Insert or update a facility record into the Facilities container.
        
        item = {
            "id": str(uuid.uuid4()),  # Unique identifier for the item
            "address": address,
            "name": name,
            "type": type_,
            "lat": lat,
            "lon": lon
        }
        self.facility_container.upsert_item(item)

    def get_cached_facilities(self, address, type_):
        
        #Query facilities from the Facilities container by address and type.
        #Returns a list of tuples with (name, type, lat, lon).
       
        query = """
        SELECT c.name, c.type, c.lat, c.lon FROM c
        WHERE c.address = @address AND c.type = @type
        """
        parameters = [
            {"name": "@address", "value": address},
            {"name": "@type", "value": type_}
        ]
        results = list(self.facility_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        return [(r['name'], r['type'], r['lat'], r['lon']) for r in results]

    def is_cached(self, address, type_):
        
        #Check if the location for the given address and type has been cached.
        #Returns True if it exists, False otherwise.
        
        query = """
        SELECT VALUE c.fetched FROM c
        WHERE c.address = @address AND c.type = @type
        """
        parameters = [
            {"name": "@address", "value": address},
            {"name": "@type", "value": type_}
        ]
        results = list(self.cache_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        return len(results) > 0

    def cache_location(self, address, type_, lat, lon, raw_json):
        #Cache the fetched location data into the LocationCache container.
        #Stores raw JSON response for potential reuse.
        
        item = {
            "id": str(uuid.uuid4()),  # Unique identifier
            "address": address,
            "type": type_,
            "fetched": True,
            "lat": lat,
            "lon": lon,
            "raw_json": json.dumps(raw_json)  # Serialize raw JSON data
        }
        self.cache_container.upsert_item(item)
