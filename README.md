*Test trên PC:
1. Chạy app.py
2. mở index.html
*Test trên Mobile:
1. Thay IP máy mình (PC) vào trong code (file: script.js) dòng: const apiUrl = `http://192.168.123.120:5000/api/locations?lat=${userLat}&lng=${userLng}&radius=${radiusInMeters}`;
2. Chạy app.py trên PC
3. Chạy index.html trên PC (click chuột phải -> Open with live server, nếu không có lựa chọn này thì tải extension Live Server của VSCode)
4. Mở trên điện thoại bằng link: http://[IP_PC]:5500.
