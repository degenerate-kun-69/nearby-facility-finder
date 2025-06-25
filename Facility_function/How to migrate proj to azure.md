# How to migrate proj to azure

1. Convert SQLite to azure cosmos DB on another git branch
2. Restructure the project 
3. restructure init.py for azure function
4. store api key in azure vault, reference in function app
5. use blob for json raw caching

| Component               | Purpose                                       |
| ----------------------- | --------------------------------------------- |
| **Azure Function**      | Entry point (runs your location finder logic) |
| **Geoapify API**        | Geocode + Facility search                     |
| **Azure Key Vault**     | Secure API key                                |
| **Azure Cosmos DB**     | Stores facility and cache data                |
| **Azure Blob Storage**  | Stores raw JSON debug files                   |
| **(Optional)** Frontend | Use React/HTML to call function via REST      |
