document.getElementById('searchButton').addEventListener('click', function(){
  var place = document.getElementById('place').value;
var mapContainer = document.getElementById('map');
var address_set = document.getElementById('addree_set');
        mapContainer.style.display = "block";
        address_set.style.display = 'flex';

        var mapOption = {
          center: new kakao.maps.LatLng(35.158, 129.163),
          level: 3
        };
        var map = new kakao.maps.Map(mapContainer, mapOption);

        var ps = new kakao.maps.services.Places();
        var geocoder = new kakao.maps.services.Geocoder();
        ps.keywordSearch(place, placesSearchCallback);

        function placesSearchCallback(data, status, pagination) {
          if (status === kakao.maps.services.Status.OK) {
            var place = data[0];
            var x = parseFloat(place.x);
            var y = parseFloat(place.y);
            var xhr = new XMLHttpRequest();
            var url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x=" + x + "&y=" + y;
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Authorization", "KakaoAK b57031084b9adfc51ceead7715839cb3");
    xhr.onload = function() {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        document.getElementById("place_address").value = response.documents[0].address_name

      }
    };
    xhr.send();
            document.getElementById("place_x").value = x;
            document.getElementById("place_y").value = y;
            var marker = new kakao.maps.Marker({
              position: new kakao.maps.LatLng(place.y, place.x)
            });
            marker.setMap(map);
            map.setCenter(marker.getPosition());
          }
        }});
