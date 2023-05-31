var container = document.getElementById('maps');
        var options = {
            center: new kakao.maps.LatLng(start_y, start_x),
            level: 3
        };

        var map = new kakao.maps.Map(container, options);

        var markerPosition = new kakao.maps.LatLng(start_y, start_x);

        var marker = new kakao.maps.Marker({
            position: markerPosition
        });

        marker.setMap(map);
