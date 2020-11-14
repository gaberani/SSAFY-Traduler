<template>
  <v-container style="padding:0;">
    <center>
			<!-- <form onsubmit="searchPlaces(); return false;"> -->
				<input style="font-family: 'SCDream5';border-bottom:1px #707070 solid;" type="text" v-model="query" placeholder="검색어를 입력해주세요." id="keyword" size="20"> 
				<button class="mapsearchbtn" style="font-family: 'SCDream5';background-color:#FF5E5E;width:20%; border-radius:10px; color:white;" @click.prevent="searchmap">검색</button> 
			<!-- </form> -->
      <div id="map2" class="map">
			</div>
    </center>
		<span style="font-family: 'SCDream5'; border-bottom:2px #FF5E5E solid; font-size:1.1rem;">{{custom_title}} </span>
  </v-container>
</template>

<script>
export default {
  name: 'CustomSpotMap',
  data() {
    return {
			// Places:{}
			query:"",
			custom_lat:'',
			custom_lon:'',
			custom_title:'',
			keyword:' ',
    }
	},
	// props: ['item'],
  mounted() {
		this.makeMap();
	},
	watch: {
		keyword() {
			this.makeMap();
		}
	},
  methods: {
		searchmap() {
			this.keyword = this.query
		},
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
			const self = this
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
			// var keyword = this.keyword
			
			ps.keywordSearch( this.keyword, placesSearchCB);
			
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
			// var customtom =[];
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
							let customspot_info = {
								"title" : place.place_name,
								"lat": place.y,
								"lon": place.x,
							}
							self.$emit("select", customspot_info)
							self.custom_lat = place.y
							self.custom_lon = place.x
							self.custom_title = place.place_name
							console.log(self.custom_lat)
							console.log(self.custom_lon)
							console.log(self.custom_title)
							infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
							infowindow.open(map, marker);
					});
			}
		},
	}
}
</script>

<style scoped>
.map {
  /* margin-left:10px; */
  width: 96%;
  height: 185px;
  border-radius:20px;
  margin-top:1%;
}
</style>
