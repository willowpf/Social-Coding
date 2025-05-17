import requests
import urllib.parse

GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

def geocoding(location, key):
    if not location:
        return 400, None, None, None

    url = GEOCODE_URL + urllib.parse.urlencode({
        "q": location,
        "limit": "1",
        "key": key
    })

    response = requests.get(url)
    if response.status_code != 200:
        return response.status_code, None, None, None

    data = response.json()
    if not data["hits"]:
        return 200, None, None, None

    hit = data["hits"][0]
    lat = hit["point"]["lat"]
    lng = hit["point"]["lng"]
    name = hit["name"]
    state = hit.get("state", "")
    country = hit.get("country", "")

    new_loc = f"{name}, {state}, {country}".strip(", ")
    return 200, lat, lng, new_loc
