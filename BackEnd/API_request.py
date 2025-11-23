import requests
import json

# Example coordinates (District 1, HCMC)
lat = 10.7769
lon = 106.7009
radius = 1000  # meters

# Overpass QL query
query = f"""
[out:json];
(
  node["amenity"="cafe"](around:{radius},{lat},{lon});
  node["tourism"="museum"](around:{radius},{lat},{lon});
);
out center;
"""

url = "https://overpass-api.de/api/interpreter"

try:
    response = requests.post(url, data=query)
    response.raise_for_status()
    data = response.json()

    elements = data.get("elements", [])

    if not elements:
        print("No POIs found nearby.")
    else:
        for el in elements:
            name = el.get("tags", {}).get("name", "Unnamed POI")
            poi_type = el.get("tags", {}).get("amenity") or el.get("tags", {}).get("tourism")
            lat = el.get("lat")
            lon = el.get("lon")

            print(f"- {name} ({poi_type}) at ({lat}, {lon})")

except Exception as e:
    print("Error:", e)
