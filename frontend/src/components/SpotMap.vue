<template>
  <v-container>
    <div :id="'map'+item" class="map"></div>
  </v-container>
</template>

<script>
export default {
  name: 'SpotMap',
  data() {
    return {
      item: ''
    }
  },
  created() {
    this.item = this.$attrs.data
  },
  mounted() {
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
  methods: {
    initMap() {
      var MapContainer = document.getElementById('map' + this.item);
      var MapOption = {
        // 지도의 좌표
        center: new kakao.maps.LatLng(37.501239, 127.039652),
        // 지도의 레벨(확대, 축소 정도)
        level: 5
      };
      // 지도 생성 및 객체 리턴
      var map = new kakao.maps.Map(MapContainer, MapOption);
      // 정적인 지도
      // var map = new kakao.maps.StaticMap(MapContainer, MapOption);

      // 여행지 간 좌표로 그려질 선 객체
      var linePath = [
        new kakao.maps.LatLng(37.50044353828887, 127.03718466576542),
        new kakao.maps.LatLng(37.50127800000000, 127.04000408677545),
        new kakao.maps.LatLng(37.50128969715334, 127.03960000000000)
      ];
      // var distanceOverlay; // 선의 거리정보를 표시할 커스텀오버레이 입니다
      // var dots = {}; // 여행지 마커 커스텀 오버레이 배열입니다.

      var polyline = new kakao.maps.Polyline({
        path: linePath,         // 선을 구성하는 좌표배열 입니다
        strokeWeight: 5,        // 선의 두께 입니다
        strokeColor: '#000000', // 선의 색깔입니다
        strokeOpacity: 0.7,     // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
        strokeStyle: 'solid'    // 선의 스타일입니다
      });
      polyline.setMap(map)

      // 드래그, 확대축소 막기
      map.setDraggable(false);
      map.setZoomable(false);

      // 지도의 타입 설정
      map.setMapTypeId(kakao.maps.MapTypeId.ROADMAP);
    }
  }
}
</script>

<style scoped>
.map {
  width: 400px;
  height: 300px;
  margin-bottom: 10px;
}
</style>