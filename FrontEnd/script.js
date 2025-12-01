document.addEventListener('DOMContentLoaded', function () {
    // --- KHỞI TẠO MAP & ICON ---
    const resIcon = L.icon({ iconUrl: 'Assets/res-icon.png', iconSize: [36, 36], shadowSize: [36, 36] });
    const cafeIcon = L.icon({ iconUrl: 'Assets/cafe-icon.png', iconSize: [36, 36], shadowSize: [36, 36] });
    const hotelIcon = L.icon({ iconUrl: 'Assets/hotel-icon.png', iconSize: [36, 36], shadowSize: [36, 36] });
    const parkIcon = L.icon({ iconUrl: 'Assets/park-icon.png', iconSize: [36, 36], shadowSize: [36, 36] });
    const museumIcon = L.icon({ iconUrl: 'Assets/museum-icon.png', iconSize: [36, 36], shadowSize: [36, 36] });
    const barIcon = L.icon({ iconUrl: 'Assets/bar-icon.png', iconSize: [36, 36], shadowSize: [36, 36] });
    const smarketIcon = L.icon({ iconUrl: 'Assets/supermarket-icon.png', iconSize: [36, 36], shadowSize: [36, 36] });
    const marketIcon = L.icon({ iconUrl: 'Assets/marketplace-icon.png', iconSize: [36, 36], shadowSize: [36, 36] });
    const libraryIcon = L.icon({ iconUrl: 'Assets/library-icon.png', iconSize: [36, 36], shadowSize: [36, 36] });
    const defaultIcon = L.icon({});

    // Mật độ giao thông
    const trafficFlowLayer = L.tileLayer(
        "https://api.tomtom.com/traffic/map/4/tile/flow/relative/{z}/{x}/{y}.png?key=l6e2nZO9QtCFvw3Gi69l2NjlwHiElGpC",
        {   opacity: 0.8, 
            maxZoom: 19,
            maxNativeZoom: 18
        }
    );
    
    const map = L.map('map').setView([10.7769, 106.7009], 13);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19, attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    let locations = [];
    const markersLayer = L.layerGroup().addTo(map);

    const detailsPanel = document.getElementById('restaurant-details');
    const placeName = document.getElementById('res-name');
    const placeAddress = document.getElementById('res-address');
    const placeDescription = document.getElementById('res-description');
    const closeBtn = document.getElementById('close-btn');

    // --- HÀM GỌI API ---
    function fetchLocations(userLat, userLng, radiusInMeters) {
        const apiUrl = `http://127.0.0.1:5000/api/locations?lat=${userLat}&lng=${userLng}&radius=${radiusInMeters}`;

        console.log(`Đang quét dữ liệu thực tế...`);

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                console.log("Dữ liệu thực tế:", data);
                locations = data;
                renderMarkers('all');
                
            })
            .catch(error => {
                console.error("Lỗi:", error);
                alert("Lỗi kết nối hoặc API quá tải.");
            });
    }

    function getIconByCategory(category) {
        if (category === 'restaurant') return resIcon;
        if (category === 'hotel') return hotelIcon;
        if (category === 'cafe') return cafeIcon;
        if (category === 'bar') return barIcon;          
        if (category === 'museum') return museumIcon;     
        if (category === 'library') return libraryIcon;      
        if (category === 'park') return parkIcon;        
        if (category === 'supermarket') return smarketIcon; 
        if (category === 'marketplace') return marketIcon;
        return defaultIcon;
    }

    function renderMarkers(type) {
        markersLayer.clearLayers();
        const filteredLocations = locations.filter(location => type === 'all' || location.category === type);

        filteredLocations.forEach(location => {
            const iconToUse = getIconByCategory(location.category);
            const marker = L.marker([location.lat, location.lng], { icon: iconToUse });
            
            marker.on('click', () => {
                placeName.textContent = location.name;
                // Hiển thị thêm khoảng cách
                placeAddress.textContent = `Cách bạn: ${location.distance} mét - Đ/c: ${location.address}`;
                placeDescription.textContent = location.description;
                detailsPanel.classList.remove('hidden');
            });
            marker.addTo(markersLayer);
        });
    }

    // Xử lý nút lọc loại
    const moreBtn = document.getElementById('more-btn');
    const dropdownMenu = document.getElementById('dropdown-menu');

    moreBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show-menu');
    });

    document.addEventListener('click', function(e) {
        if (!dropdownMenu.contains(e.target) && e.target !== moreBtn) {
            dropdownMenu.classList.remove('show-menu');
        }
    });

    const allTagButtons = document.querySelectorAll('.tag-btn');
    
    allTagButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            if (this.id === 'more-btn') return;

            allTagButtons.forEach(b => b.classList.remove('active'));

            this.classList.add('active');

            if (this.classList.contains('dropdown-item')) {
                moreBtn.classList.add('active');
                dropdownMenu.classList.remove('show-menu');
            }

            const type = this.getAttribute('data-type');
            renderMarkers(type);
        });
    });

    closeBtn.addEventListener('click', () => detailsPanel.classList.add('hidden'));
    

    const trafficBtn = document.getElementById('traffic-toggle');
    trafficFlowLayer.addTo(map);
    trafficBtn.addEventListener('click', function() {
        if (map.hasLayer(trafficFlowLayer)) {
            map.removeLayer(trafficFlowLayer);
            this.classList.remove('active');
        } else {
            trafficFlowLayer.addTo(map);
            this.classList.add('active');
        }
    });
    
    // 1. Kiểm tra Geolocation
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const lat = pos.coords.latitude;
                const lng = pos.coords.longitude;

                // Di chuyển map về chỗ người dùng
                map.setView([lat, lng], 15);
                L.marker([lat, lng]).addTo(map).bindPopup('Bạn ở đây').openPopup();

                // 2. GỌI API LẤY DỮ LIỆU
                // Tìm trong bán kính 1000 mét
                fetchLocations(lat, lng, 1000); 
            },
            // THẤT BẠI (User chặn vị trí)
            (error) => {
                alert("Bạn cần cho phép vị trí để tìm quán quanh đây. Đang dùng vị trí mặc định tại TP.HCM");
                // Dùng vị trí mặc định (Quận 1) nếu user chặn
                fetchLocations(10.7769, 106.7009, 1000);
            }
        );
    } else {
        alert("Trình duyệt không hỗ trợ vị trí.");
    }
});
