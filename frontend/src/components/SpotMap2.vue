<template>
  <v-container style="padding:0;">
    <center>
      <div id="map" class="map"></div>
    </center>
  </v-container>
</template>

<script>
export default {
  name: 'SpotMap2',
  data() {
    return {
      // item: '',
      // SDdetail:[],
    }
	},
	props: ['SDdetail','item'],
  mounted() {
		this.makeMap();
	},
	watch: {
		item() {
			this.makeMap();
		}
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
      script.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${process.env.VUE_APP_KAKAO_MAP_JS_KEY}`;
      document.head.appendChild(script);
    }
		},
    initMap() {
      var MapContainer = document.getElementById('map');
      var MapOption = {
        // 지도의 좌표
        center: new kakao.maps.LatLng(this.SDdetail.avg_coord[0], this.SDdetail.avg_coord[1]),
        // 지도의 레벨(확대, 축소 정도)
        level: 10
      };
      // 지도 생성 및 객체 리턴
      var map = new kakao.maps.Map(MapContainer, MapOption);
      // 정적인 지도
      // var map = new kakao.maps.StaticMap(MapContainer, MapOption);

      // 여행지 간 좌표로 그려질 선 객체
      var linePath = [];
			var Positions = [];
      for (var i=0; i<this.SDdetail.course_coords.length; i++) {
				linePath.push(new kakao.maps.LatLng(this.SDdetail.course_coords[i][0], this.SDdetail.course_coords[i][1])); 
				Positions.push({title:"추가할거야~",latlng:new kakao.maps.LatLng(this.SDdetail.course_coords[i][0], this.SDdetail.course_coords[i][1])});   
        }
        // console.log(linePath)
      // var distanceOverlay; // 선의 거리정보를 표시할 커스텀오버레이 입니다
      // var dots = {}; // 여행지 마커 커스텀 오버레이 배열입니다.
			
      var polyline = new kakao.maps.Polyline({
        path: linePath,         // 선을 구성하는 좌표배열 입니다
        strokeWeight: 5,        // 선의 두께 입니다
        strokeColor: '#FF1313', // 선의 색깔입니다
        strokeOpacity: 0.7,     // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
        strokeStyle: 'solid'    // 선의 스타일입니다
			});
			for (var j = 0; j < Positions.length; j ++) { 
    
			// 마커를 생성합니다
			var marker = new kakao.maps.Marker({
					map: map, // 마커를 표시할 지도
					position: Positions[j].latlng, // 마커를 표시할 위치
					title : Positions[j].title, // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다 
				});
			}
      polyline.setMap(map)
			marker.setMap(map);
      // 드래그, 확대축소 막기
    //   map.setDraggable(false);
    //   map.setZoomable(false);

      // 지도의 타입 설정
      map.setMapTypeId(kakao.maps.MapTypeId.ROADMAP);
    },
  }
}
</script>

<style scoped>
.map {
  /* margin-left:10px; */
  width: 96%;
  height: 40vw;
  border-radius:20px;
}
</style>
