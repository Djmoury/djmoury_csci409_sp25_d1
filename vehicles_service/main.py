from fastapi import FastAPI, Depends
import httpx

API_KEY = "ff227ff12fca4c059e83f728c8a7f7fb"  
ENDPOINT_URL = "https://api-v3.mbta.com" 

app = FastAPI()

# Dependency to fetch all vehicles with optional filters for route and in-service status
async def get_all_vehicles(route: str = None, revenue: bool = None):
    params = {"api_key": API_KEY}
    if route:
        params["filter[route]"] = route
    if revenue is not None:
        params["filter[is_in_service]"] = "true" if revenue else "false"

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/vehicles", params=params)
        response.raise_for_status()
        return response.json()

@app.get("/vehicles")
async def read_vehicles(
    route: str = None, 
    revenue: bool = None, 
    vehicles=Depends(get_all_vehicles)
):
    return vehicles
