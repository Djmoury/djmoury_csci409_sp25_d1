from fastapi import FastAPI, Depends
import httpx

API_KEY = "ff227ff12fca4c059e83f728c8a7f7fb" 
ENDPOINT_URL = "https://api-v3.mbta.com"

app = FastAPI()


async def get_all_alerts(route: str = None, stop: str = None):
    params = {"api_key": API_KEY}
    if route:
        params["filter[route]"] = route
    if stop:
        params["filter[stop]"] = stop

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/alerts", params=params)
        response.raise_for_status()
        return response.json()

@app.get("/alerts")
async def read_alerts(
    route: str = None, 
    stop: str = None, 
    alerts=Depends(get_all_alerts)
):
    return alerts

