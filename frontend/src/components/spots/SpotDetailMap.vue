<template>
  <v-container style="padding:0;">
    <div id="map" class="map"></div>
  </v-container>
</template>

<script>
export default {
  name: 'SpotDetailMap',
  props: {
    lat: {
      type: Number
    },
    lon: {
      type: Number
    }
  },
  mounted() {
    this.makeMap();
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
      var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
        mapOption = { 
          center: new kakao.maps.LatLng(this.lat, this.lon), // 지도의 중심좌표
          level: 3 // 지도의 확대 레벨
        };

      var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

      // 드래그, 확대축소 막기
      // map.setDraggable(false);
      // map.setZoomable(false);
      // 지도의 타입 설정
      map.setMapTypeId(kakao.maps.MapTypeId.ROADMAP);

      // 마커가 표시될 위치입니다 
      var markerPosition  = new kakao.maps.LatLng(this.lat, this.lon); 

      // 마커를 생성합니다
      var marker = new kakao.maps.Marker({
        position: markerPosition
      });

      // 마커가 지도 위에 표시되도록 설정합니다
      marker.setMap(map);
    }
  },
  watch: {
    lat() {
      this.makeMap();
    }
  },
}
</script>

<style scoped>
.map {
  width: 100%;
  height: 18vw;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
}
</style>
