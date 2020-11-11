<template>
  <v-container>
		<h2>스케줄 페이지</h2>
    <div v-for="item in items" :key="item">
      <SpotMap :data="item"></SpotMap>
    </div>
	</v-container>
</template>

<script>
import SpotMap from '@/components/SpotMap.vue'
// const DAUM_KAKAO_URL = `//dapi.kakao.com/v2/maps/sdk.js?appkey=&libraries=drawing,clusterer,services&autoload=false`

export default {
	name: 'Schedule',
  components: {SpotMap},
  data() {
		return {
			items: ['a', 'b', 'c', 'd']
		}
	},
}
</script>

<style>
</style>