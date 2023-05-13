window.onload = function(){
    document.getElementById("place").addEventListener("click", function(){ //주소입력칸을 클릭하면
        //카카오 지도 발생
        new daum.Postcode({
            oncomplete: function(data) { //선택시 입력값 세팅
                document.getElementById("place").value = data.address; // 주소 넣기
                var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapOption = {
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };
                document.getElementById("map").style.display = "block";

// 지도를 생성합니다
var map = new kakao.maps.Map(mapContainer, mapOption);

// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();

// 주소로 좌표를 검색합니다
geocoder.addressSearch(data.address, function(result, status) {

    // 정상적으로 검색이 완료됐으면
     if (status === kakao.maps.services.Status.OK) {

        var coord = new kakao.maps.LatLng(result[0].y, result[0].x);

        var marker = new kakao.maps.Marker({
            map: map,
            position: coord
        });

        // 인포윈도우로 장소에 대한 설명을 표시합니다
        var infowindow = new kakao.maps.InfoWindow({
            content: '<div style="width:150px;text-align:center;padding:6px 0;">출발지</div>'
        });
        infowindow.open(map, marker);

        // 결과값으로 받은 위치를 마커로 표시합니다
         map.setCenter(coord);
    }
});
            }
        }).open();
    });}