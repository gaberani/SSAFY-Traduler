<template>
  <v-container>
		<h2>스케쥴 페이지</h2>
    <div v-for="item in items" :key="item">
      <div :id="'map'+item" class="map"></div>
    </div>
	</v-container>
</template>

<script>
// const DAUM_KAKAO_URL = `//dapi.kakao.com/v2/maps/sdk.js?appkey=&libraries=drawing,clusterer,services&autoload=false`

export default {
	name: 'Schedule',
	data() {
		return {
			items: ['a', 'b', 'c']
		}
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
      this.items.forEach(item => {
        var container = document.getElementById('map'+item);
        var options = {
          // 지도의 좌표
          // center: new kakao.maps.LatLng(33.450701, 126.570667),
          center: new kakao.maps.LatLng(37.501239, 127.039652),
          // 지도의 레벨(확대, 축소 정도)
          level: 3
        };
        // 지도 생성 및 객체 리턴
        var map = new kakao.maps.Map(container, options);
        // 정적인 지도
        // var staticMap = new kakao.maps.StaticMap(staticMapContainer, staticMapOption);
        // ??
        map.setMapTypeId(kakao.maps.MapTypeId.HYBRID);
      })
    },
    // HTML Content를 만들어 리턴하는 함수입니다
    // getTimeHTML(distance) {
    //   // 도보의 시속은 평균 4km/h 이고 도보의 분속은 67m/min입니다
    //   var walkkTime = distance / 67 | 0;
    //   var walkHour = '', walkMin = '';
    //
    //   // 계산한 도보 시간이 60분 보다 크면 시간으로 표시합니다
    //   if (walkkTime > 60) {
    //     walkHour = '<span class="number">' + Math.floor(walkkTime / 60) + '</span>시간 '
    //   }
    //   walkMin = '<span class="number">' + walkkTime % 60 + '</span>분'
    //
    //   // 자전거의 평균 시속은 16km/h 이고 이것을 기준으로 자전거의 분속은 267m/min입니다
    //   var bycicleTime = distance / 227 | 0;
    //   var bycicleHour = '', bycicleMin = '';
    //
    //   // 계산한 자전거 시간이 60분 보다 크면 시간으로 표출합니다
    //   if (bycicleTime > 60) {
    //     bycicleHour = '<span class="number">' + Math.floor(bycicleTime / 60) + '</span>시간 '
    //   }
    //   bycicleMin = '<span class="number">' + bycicleTime % 60 + '</span>분'
    //
    //   // 거리와 도보 시간, 자전거 시간을 가지고 HTML Content를 만들어 리턴합니다
    //   var content = '<ul class="dotOverlay distanceInfo">';
    //   content += '    <li>';
    //   content += '        <span class="label">총거리</span><span class="number">' + distance + '</span>m';
    //   content += '    </li>';
    //   content += '    <li>';
    //   content += '        <span class="label">도보</span>' + walkHour + walkMin;
    //   content += '    </li>';
    //   content += '    <li>';
    //   content += '        <span class="label">자전거</span>' + bycicleHour + bycicleMin;
    //   content += '    </li>';
    //   content += '</ul>'
    // }
  }
}
</script>

<style>
.map {
  width: 400px;
  height: 300px;
  margin-bottom: 10px;
}
</style>