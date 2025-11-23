import requests
import json

# 🔑 Put your real OpenTripMap API key here
API_KEY = "5ae2e3f221c38a28845f05b644c5bf898d1c02ec9cfe9561514497c5"

# 📍 Set coordinates somewhere with known POIs
lat = 10.776889      # Example: District 1, HCMC
lon = 106.700806
radius = 5000         # meters
limit = 10            # number of POIs to fetch
kinds = "Architecture"


# Step 1: Get nearby POIs
def get_nearby_pois(lat, lon, radius, limit, kinds):
    url = "https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "limit": limit,
        "kinds": kinds,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("Error fetching POIs:", response.status_code, response.text)
        return []

    data = response.json()
    return data.get("features", [])

# Step 2: Get detailed info for each POI
def get_poi_details(xid):
    url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}"
    params = {"apikey": API_KEY}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching details for {xid}: {response.status_code}")
        return {}
    
    return response.json()

# Step 3: Run the process
pois = get_nearby_pois(lat, lon, radius, limit, kinds)

if not pois:
    print("No POIs found. Try increasing radius or checking coordinates.")
else:
    print(f"Found {len(pois)} POIs:\n")
    for i, poi in enumerate(pois, start=1):
        props = poi["properties"]
        name = props.get("name", "Unnamed")
        xid = props.get("xid")
        kind = props.get("kinds", "Unknown")
        dist = props.get("dist", "?")
        
        print(f"{i}. {name} | Category: {kind} | Distance: {dist}m | XID: {xid}")
        
        details = get_poi_details(xid)
        desc = details.get("wikipedia_extracts", {}).get("text", "No description available")
        photo = details.get("preview", {}).get("source", "No photo available")
        
        print(f"   Description: {desc[:100]}...")  # first 100 chars
        print(f"   Photo URL: {photo}\n")
