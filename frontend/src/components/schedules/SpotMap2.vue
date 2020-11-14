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
		},
		SDdetail: {
			deep: true,
			handler() {
				this.initMap();
			}
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
      script.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${process.env.VUE_APP_KAKAO_MAP_JS_KEY}&libraries=services,clusterer,drawing`;
      document.head.appendChild(script);
    }
		},
		// gotodetailspot() {
		// 	console.log('111111111111111111')
		// 	// this.$router.push({name:'SpotDetail', params: {spot_id: pk} })
		// },
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
				if (this.SDdetail.course[i].spot_pk !=null){
					linePath.push(new kakao.maps.LatLng(this.SDdetail.course_coords[i][0], this.SDdetail.course_coords[i][1])); 
					Positions.push({title:this.SDdetail.course[i].spot_info.title,
					latlng:new kakao.maps.LatLng(this.SDdetail.course_coords[i][0], this.SDdetail.course_coords[i][1]),
					address:this.SDdetail.course[i].spot_info.address,
					image:this.SDdetail.course[i].spot_info.image,
					id:this.SDdetail.course[i].spot_info.id,
					course: i+1,
					});
				} else {
					{
					linePath.push(new kakao.maps.LatLng(this.SDdetail.course_coords[i][0], this.SDdetail.course_coords[i][1])); 
					Positions.push({title:this.SDdetail.course[i].custom_spot_info.title,
					latlng:new kakao.maps.LatLng(this.SDdetail.course_coords[i][0], this.SDdetail.course_coords[i][1]),
					// address:this.SDdetail.course[i].spot_info.address,
					// image:this.SDdetail.course[i].cspot_info.image,
					id:this.SDdetail.course[i].custom_spot_info.id,
					course: i+1,
					});
				}  
				}
				// title:this.SDdetail.course[i].spot_info.title,
			}
        // console.log(linePath)
      // var distanceOverlay; // 선의 거리정보를 표시할 커스텀오버레이 입니다
      // var dots = {}; // 여행지 마커 커스텀 오버레이 배열입니다.
			var bounds = new kakao.maps.LatLngBounds();
      for (i = 0; i < this.SDdetail.course_coords.length; i++) {
          // LatLngBounds 객체에 좌표를 추가합니다
          bounds.extend(linePath[i]);
      }
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
				});
				if (Positions[j].address) {
					var iwContent='<div style="width:350px; font-family: SCDream5;">' 
					+'<button style="color:white; margin-top:3px; width:25px; height:25px; border-radius:100%; background-color:#FF5E5E; margin-right:10px;">'+ Positions[j].course + ' </button>'
					+ Positions[j].title + '<br>' 
					+ '<span style="font-size:0.9rem; font-family: SCDream4;">' +Positions[j].address +'</span>' 
					+ '<img style="width:300px;" src="' +Positions[j].image + '"/>'
					// + '<button id="test1" style="margin-bottom:5px; display:block; background-color:#FF5E5E; width:100px; border-radius:10px; color:white;">상세보기</button>' 
					+'</div>'
					var infowindow = new kakao.maps.InfoWindow({
					content: iwContent, // 인포윈도우에 표시할 내용
					removable :true
					
					});
					kakao.maps.event.addListener(marker, 'click', makeOverListener(map, marker, infowindow));
					var iwContent2='<div style="width:320px; font-family: SCDream4;">' 
					+'<button style="color:white; margin-top:3px; width:25px; height:25px; border-radius:100%; background-color:#FF5E5E; margin-right:10px;">'+ Positions[j].course + ' </button>'
					+ Positions[j].title 
					+ '<p style="font-family: SCDream4; margin:0px; color:#707070; font-size:0.8rem;">자세히 보려면 마커를 눌러주세요.</p>' +'</div>' 
					
					var infowindow2 = new kakao.maps.InfoWindow({
					content: iwContent2, // 인포윈도우에 표시할 내용
					});
						kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker, infowindow2));
						// kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow));
						kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow2));
				
				} else {
				var iwContent3='<div style="width:320px; font-family: SCDream4;">' 
				+'<button style="color:white; margin-top:3px; width:25px; height:25px; border-radius:100%; background-color:#FF5E5E; margin-right:10px;">'+ Positions[j].course + ' </button>'
				+ Positions[j].title 
				
				var infowindow3 = new kakao.maps.InfoWindow({
				content: iwContent3, // 인포윈도우에 표시할 내용
				});
						kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker, infowindow3));
						// kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow));
						kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow3));
				}
			}
			function makeOverListener(map, marker, infowindow) {
					return function() {
							infowindow.open(map, marker);
					};
			}

			// 인포윈도우를 닫는 클로저를 만드는 함수입니다 
			function makeOutListener(infowindow) {
					return function() {
							infowindow.close();
					};
			}
			if (this.SDdetail.course_coords.length !=0){
				polyline.setMap(map)
				marker.setMap(map);
				map.setBounds(bounds);
			}
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
  height: 660px;
  border-radius:20px;
  margin-top:5%;
}
</style>
