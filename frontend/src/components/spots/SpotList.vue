<template>
  <div class="spotlist">
    <div>
      <div class="mb-3 mt-3">
        <h1 style="display:inline; color:#FF5E5E; font-size:2.7vw;">추천</h1>
        <h3 style="display:inline; font-size:1.7vw;"> {{ recom_area }} 여행지</h3>
      </div>
      <div v-for="recom_spot in recom_spots" :key="recom_spot.id" style="display:inline;" >
        <SpotCard :spot="recom_spot" />
      </div>
    </div>
    <div>
      <div class="mb-3 mt-2">
        <h1 style="display:inline; color:#FF9617; font-size:2.7vw;">BEST</h1>
        <h3 style="display:inline; font-size:1.7vw;"> 여행지</h3>
      </div>
      <div v-for="best_spot in best_spots" :key="best_spot.id" style="display:inline;" >
        <button class="besttag" >BEST</button>
        <SpotCard :spot="best_spot" />
      </div>
    </div>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  import axios from 'axios'

  import SpotCard from '@/components/spots/SpotCard';
  import SERVER from '@/api/api'

  export default {
    data () {
      return {
        recom_area: '',
        recom_spots: [],
        best_spots: [],
      }
    },
    components: {
      SpotCard,
    },
    computed: {
      ...mapGetters('accounts', ['LoginFlag', 'config']),
      headers() {
        return (this.LoginFlag ? {headers: {Authorization: this.config}} : null)
      }
    },
    created() {
      this.get_recommend_spots();
      this.get_best_spots();
    },
    methods: {
      get_recommend_spots() {
        axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.RECOMMEND, this.headers)
        .then(res => {
          this.recom_area = res.data.recom_area
          this.recom_spots = res.data.recom_spots.slice(0, 3);
        })
        .catch(err => console.log(err.response))
      },
      get_best_spots() {
        axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.BEST, this.headers)
        .then(res => {
          this.best_spots = res.data.slice(0, 3);
        })
        .catch(err => console.log(err.response))
      }
    }
  }
</script>

<style>
.spotlist {
    margin-top: 2%;
    width:66.6666666%;
    margin-left:16.6666666%;
}
.plusbtn {
    float:right;
    margin-top:18px;
    width:6%;
    font-size:1vw;
    height:2.5vw;
    border-radius:20px;
    background-color: #FF5E5E;
    color:white;
    outline:none;
    font-family: 'SCDream6'
}
.besttag {
    z-index:1; 
    /* background-color:#FF9617;  */
    position:absolute; float:left; 
    transform: rotate(-45deg); 
    margin-left:-2.4%; 
    margin-top:2%; 
    height:3vw; 
    width:13%;
    font-size:2.1vw;
    font-family: 'SCDream6';
    color:white;
    border-left: 3vw solid transparent;
    border-right: 3vw solid transparent;
    border-bottom: 3vw solid #FF9617;
    outline: none;
}
</style>