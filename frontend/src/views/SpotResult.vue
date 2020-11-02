<template>
  <v-app>
		<SearchSpot/>
			<div class="spotresult">
				<div>
					<h1 class="mb-5" style="color:#FF5E5E;font-size:2.4vw;">검색 결과</h1>
				</div>
				<div v-for="spot in spots" :key="spot.id" style="display:inline;">
					<!-- v-for -->
					<SpotCard :spot="spot"/>
				</div>
				<div class="text-center">
					<v-pagination
						v-model="page"
						:length="spotspage.endPage"
						:total-visible="7"
						class="mt-5"
					></v-pagination>
				</div>
			</div>
		<Footer/>
  </v-app>
</template>

<script>
import SearchSpot from '@/components/SearchSpot';
import Footer from '@/components/Footer';
import SpotCard from '@/components/SpotCard';
import axios from 'axios'
import { mapGetters } from "vuex";
export default {
	components:{SearchSpot, Footer,SpotCard},
	computed: {
		...mapGetters(["config","LoginFlag"]),
	},
	watch: {
		page() {
			this.getSpotList();}
	},
	data () {
		return {
			page: 1,
			spots: [],
			spotspage: [],
		}
	},
	methods: {
		getSpotList() {
			if (this.LoginFlag){const params = new URL(document.location).searchParams;
			axios.get(`http://127.0.0.1:8000/spots?title=${params.get('title')}&category=${params.get('category')}&area=${params.get('area')}&curPage=`+this.page,{
                headers: {
                    Authorization: this.config,
                },
            })
				.then(response => {
				this.spots = response.data.result
				this.spotspage = response.data.page
				console.log(this.spotspage)
				console.log(this.spots)
				})
				.catch(error => {
				console.log(error.response)
				})
			}else {
				const params = new URL(document.location).searchParams;
			axios.get(`http://127.0.0.1:8000/spots?title=${params.get('title')}&category=${params.get('category')}&area=${params.get('area')}`)
				.then(response => {
				this.spots = response.data.result
				this.spotspage = response.data.page
				console.log(this.spotspage)
				console.log(this.spots)
				})
				.catch(error => {
				console.log(error.response)
				})
			}
		}
	},
	created(){
			this.getSpotList();
		},
}
</script>

<style>
.spotresult {
	margin-top: 2%;
	width:66.6666666%;
	margin-left:16.6666666%;
}
</style>