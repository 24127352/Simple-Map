from flask import Flask, render_template, jsonify, request
# Import các hàm xử lý logic từ geo_service.py
from geo_service import search_location, find_route

app = Flask(__name__)

# --- ENDPOINT: TÌM KIẾM ĐỊA ĐIỂM ---
@app.route('/geo_service/search', methods=['GET'])
def search_location_route():
    """
    Xử lý request tìm kiếm từ client.
    Tham số: q (query string)
    """
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400
    
    # Gọi hàm xử lý logic trong geo_service.py
    data = search_location(query)
    
    if data:
        # Trả về kết quả tìm kiếm (lat, lon, display_name)
        return jsonify(data)
    
    return jsonify({"error": "Location not found"}), 404

# --- ENDPOINT: TÌM ĐƯỜNG ---
@app.route('/geo_service/route', methods=['GET'])
def find_route_route():
    """
    Xử lý request tìm đường từ client.
    Tham số: start_lat, start_lon, dest_lat, dest_lon
    """
    start_lat = request.args.get('start_lat')
    start_lon = request.args.get('start_lon')
    dest_lat = request.args.get('dest_lat')
    dest_lon = request.args.get('dest_lon')

    if not all([start_lat, start_lon, dest_lat, dest_lon]):
        return jsonify({"error": "Missing coordinates"}), 400
    
    try:
        # Chuyển đổi sang float và đóng gói thành tuple
        start = (float(start_lat), float(start_lon))
        dest = (float(dest_lat), float(dest_lon))
    except ValueError:
        return jsonify({"error": "Invalid coordinate format"}), 400

    # Gọi hàm xử lý logic trong geo_service.py
    route_coords = find_route(start, dest)
    
    if route_coords:
        # Trả về mảng các tọa độ đường đi
        return jsonify({"coordinates": route_coords})
    
    return jsonify({"error": "Could not find route"}), 404

# --- ROUTE: TRANG CHỦ ---
@app.route('/')
def index():
    """
    Render file HTML giao diện chính.
    """
    return render_template('index.html')

if __name__ == '__main__':
    # Chạy ứng dụng Flask trên cổng mặc định (5000)
    # Lưu ý: Bạn cần tạo thư mục 'templates' và đặt 'index.html' vào đó.
    app.run(debug=True)