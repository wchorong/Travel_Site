var mapContainer = document.getElementById('maps'), // 지도를 표시할 div
    mapOption = {
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };

// 지도를 생성합니다
var map = new kakao.maps.Map(mapContainer, mapOption);

// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();
// 주소로 좌표를 검색합니다
geocoder.addressSearch(start, function(result, status) {

    // 정상적으로 검색이 완료됐으면
     if (status === kakao.maps.services.Status.OK) {

        var coord = new kakao.maps.LatLng(result[0].y, result[0].x);

        // 결과값으로 받은 위치를 마커로 표시합니다
        var marker = new kakao.maps.Marker({
            map: map,
            position: coord
        });
        map.setCenter(coord);

        var bounds = new kakao.maps.LatLngBounds();
        bounds.extend(coord);
        map.setBounds(bounds);


    }

});
