<template>
  <v-container style="padding:0;">
    <div id="map2" class="map"></div>
  </v-container>
</template>

<script>
export default {
  name: 'SpotDetailMap',
  props: ['lat', 'lon', 'item'],
  mounted() {
    this.makeMap();
  },
  watch: {
    lat() {
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
      let mapContainer = document.getElementById("map2"), // 지도를 표시할 div 
        mapOption = { 
          center: new kakao.maps.LatLng(this.lat, this.lon), // 지도의 중심좌표
          level: 3 // 지도의 확대 레벨
        };

      let map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

      // 드래그, 확대축소 막기
      // map.setDraggable(false);
      // map.setZoomable(false);
      // 지도의 타입 설정
      map.setMapTypeId(kakao.maps.MapTypeId.ROADMAP);
      
      const self = this;
      setTimeout(function() {
        // 마커가 표시될 위치입니다 
        let markerPosition  = new kakao.maps.LatLng(self.lat, self.lon); 

        // 마커를 생성합니다
        let marker = new kakao.maps.Marker({
          position: markerPosition
        });
        

        // 마커가 지도 위에 표시되도록 설정합니다
        marker.setMap(map);

        map.relayout();
        map.setCenter(markerPosition);
      }, 10);
      
    }
  },
}
</script>

<style scoped>
.map {
  width: 100%;
  height: 206px;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
}
</style>
