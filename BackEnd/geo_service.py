import requests

# API Nominatim để tìm kiếm địa điểm (Geocoding)
NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'
# API OSRM để tìm đường (Routing)
OSRM_URL = 'https://router.project-osrm.org/route/v1/driving'
HEADERS = {'User-Agent': 'WebMapApplication_VN/1.0 (contact@example.com)'}

def search_location(query):
    """
    Tìm kiếm tọa độ (lat, lon) và tên hiển thị của một địa điểm.
    """
    params = {
        'format': 'json',
        'q': query,
        'limit': 1
    }
    try:
        # Sử dụng HEADERS đã định nghĩa
        response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS)
        response.raise_for_status() 
        data = response.json()
        
        if data:
            result = data[0]
            return {
                "lat": float(result['lat']),
                "lon": float(result['lon']),
                "display_name": result.get('display_name', 'Địa điểm tìm kiếm')
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error searching location: {e}")
        return None

def find_route(start_coords, dest_coords):
    """
    Tìm đường đi giữa hai tọa độ.
    """
    start_lat, start_lon = start_coords
    dest_lat, dest_lon = dest_coords
    
    coordinates_str = f"{start_lon},{start_lat};{dest_lon},{dest_lat}"
    
    params = {
        'overview': 'full',
        'geometries': 'geojson'
    }

    try:
        url = f"{OSRM_URL}/{coordinates_str}"
        # Sử dụng HEADERS
        response = requests.get(url, params=params, headers=HEADERS)
        response.raise_for_status() 
        data = response.json()
        
        if data.get('routes'):
            route = data['routes'][0]
            # Tọa độ OSRM là [lon, lat], chuyển về Leaflet [lat, lon]
            coords = [[c[1], c[0]] for c in route['geometry']['coordinates']]
            return coords
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error finding route: {e}")
        return None