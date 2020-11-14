<template>
  <v-container style="padding:0;">
    <center>
			<form onsubmit="searchPlaces(); return false;">
				<input style="font-family: 'SCDream5';border-bottom:1px #707070 solid;" type="text" value="이태원" placeholder="검색어를 입력해주세요." id="keyword" size="20"> 
				<button class="mapsearchbtn" style="font-family: 'SCDream5';background-color:#FF5E5E;width:20%; border-radius:10px; color:white;" type="">검색</button> 
			</form>
      <div id="map2" class="map">
			</div>
    </center>
		<h3>{{custom_title}} </h3>
  </v-container>
</template>

<script>
export default {
  name: 'CustomSpotMap',
  data() {
    return {
			// Places:{}
			custom_lat:'',
			custom_lon:'',
			custom_title:'123',
    }
	},
	// props: ['item'],
  mounted() {
		this.makeMap();
	},
	watch: {
	},
  methods: {
		makeMap() {
			if (window.kakao && window.kakao.maps) {
      // kakao와 kakao.maps가 전부 로딩된 뒤에 실행
      this.initMap();
    } else {
      const script = document.createElement('script');
      /* global kakao */
      script.onload = () => kakao.maps.load(this.initMap);
			// script.src=`http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${process.env.VUE_APP_KAKAO_MAP_JS_KEY}&libraries=services,clusterer,drawing`;
			// script.src=`http://dapi.kakao.com/v2/maps/sdk.js?appkey=${process.env.VUE_APP_KAKAO_MAP_JS_KEY}&libraries=services,clusterer,drawing`;
			// script.src=`//dapi.kakao.com/v2/maps/sdk.js?appkey=${process.env.VUE_APP_KAKAO_MAP_JS_KEY}&libraries=services`;
      document.head.appendChild(script);
    }
		},
    initMap() {
      var infowindow = new kakao.maps.InfoWindow({zIndex:1});

			var mapContainer = document.getElementById('map2'), // 지도를 표시할 div 
					mapOption = {
							center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
							level: 5 // 지도의 확대 레벨
					};  

			// 지도를 생성합니다    
			var map = new kakao.maps.Map(mapContainer, mapOption); 

			// 장소 검색 객체를 생성합니다
			var ps = new kakao.maps.services.Places(); 
			searchPlaces();
			// 키워드로 장소를 검색합니다
			// ps.keywordSearch('이태원 맛집', placesSearchCB); 
			function searchPlaces() {

				var keyword = document.getElementById('keyword').value;

				if (!keyword.replace(/^\s+|\s+$/g, '')) {
						// alert('키워드를 입력해주세요!');
						return false;
				}

				// 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
				ps.keywordSearch( keyword, placesSearchCB);
				// return false;
			}
			// 키워드 검색 완료 시 호출되는 콜백함수 입니다
			function placesSearchCB (data, status) {
					if (status === kakao.maps.services.Status.OK) {

							// 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
							// LatLngBounds 객체에 좌표를 추가합니다
							var bounds = new kakao.maps.LatLngBounds();

							for (var i=0; i<data.length; i++) {
									displayMarker(data[i]);    
									bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
							}       

							// 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
							map.setBounds(bounds);
					} 
			}
			var customtom =[];
			// 지도에 마커를 표시하는 함수입니다
			function displayMarker(place) {
					
					// 마커를 생성하고 지도에 표시합니다
					var marker = new kakao.maps.Marker({
							map: map,
							position: new kakao.maps.LatLng(place.y, place.x) 
					});
					// 마커에 클릭이벤트를 등록합니다
					kakao.maps.event.addListener(marker, 'click', function() {
							// 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
							console.log(customtom,place)
							customtom = place
							infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
							infowindow.open(map, marker);
					});
			}
			console.log(customtom)
			this.custom_lat = customtom.y
			this.custom_lon = customtom.x
			this.custom_title = customtom.place_name
			console.log(this.custom_lat)
			console.log(this.custom_lon)
			console.log(this.custom_title)
		},
		// makeCustomspot(place) {
		// 	this.custom_lat = place.y
		// 	this.custom_lon = place.x
		// 	this.custom_title = place.place_name
		// 	console.log(this.custom_lat)
		// 	console.log(this.custom_lon)
		// 	console.log(this.custom_title)
		// }
	}
}
</script>

<style scoped>
.map {
  /* margin-left:10px; */
  width: 96%;
  height: 200px;
  border-radius:20px;
  margin-top:1%;
}
</style>
