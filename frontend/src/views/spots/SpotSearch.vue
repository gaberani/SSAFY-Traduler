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
          v-model="curPage"
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
  import axios from 'axios'
  import { mapGetters } from "vuex";
  import SERVER from '@/api/api'

  import SearchSpot from '@/components/spots/SearchSpot';
  import SpotCard from '@/components/spots/SpotCard';
  import Footer from '@/components/Footer';

  export default {
    data () {
      return {
        spots: [],
        spotspage: [],
        curPage: 1
      }
    },
    components:{
      SearchSpot,
      Footer,
      SpotCard
    },
    computed: {
      ...mapGetters(["config", "LoginFlag"]),
      headers() {
        return (this.LoginFlag ? {Authorization: this.config} : null)
      },
    },
    watch: {
      curPage() {
        this.movePage();
      }
    },
    methods: {
      getSpotList() {
        axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.SPOTS, {
          params: {
            title: this.$route.query.title,
            category: this.$route.query.category,
            area: this.$route.query.area,
            curPage: this.$route.query.curPage
          },
          headers: this.headers
        })
        .then(res => {
          this.spots = res.data.result;
          this.spotspage = res.data.page;
        })
        .catch(err => console.log(err.response))
      },
      movePage() {
        this.$router.push({ query: {
          title: this.$route.query.title,
          category: this.$route.query.category,
          area: this.$route.query.area,
          curPage: this.curPage
          }
        }).catch(()=>{})
      }
    },
    created(){
      this.getSpotList();
      this.curPage = this.$route.query.curPage * 1
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