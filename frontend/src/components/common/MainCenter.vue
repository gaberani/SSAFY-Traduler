<template>
  <div class="maincenter">
      <div>
        <div class="mb-3 mt-3">
            <h1 style="display:inline; color:#FF5E5E; font-size:2.7vw;">함께 </h1>
            <h3 style="display:inline; font-size:1.7vw; ">떠나요</h3>
            <!-- 나중에 이모티콘으로 교체 버튼 임시 -->
            <img src="@/assets/friend.png" style="margin-left: 8px;margin-bottom: -0.5vw; height: 2vw; filter:saturate(150%);" >
            <span class="imo"> 동행 모집</span>
            <img src="@/assets/help2.png" style="margin-left: 8px; margin-bottom: -0.5vw; height: 2vw; filter:saturate(150%);">
            <span class="imo"> 도움 요청</span>
            <router-link :to="{name: 'ScheduleMain'}"><button class="plusbtn">더보기</button></router-link>
            <div>
                <button class="mainspotbtn" @click="SelectArea('')">전체</button>
                <button class="mainspotbtn" @click="SelectArea('A')">서울</button>
                <button class="mainspotbtn" @click="SelectArea('B')">인천</button>
                <button class="mainspotbtn" @click="SelectArea('C')">대전</button>
                <button class="mainspotbtn" @click="SelectArea('D')">대구</button>
                <button class="mainspotbtn" @click="SelectArea('E')">광주</button>
                <button class="mainspotbtn" @click="SelectArea('F')">부산</button>
                <button class="mainspotbtn" @click="SelectArea('G')">울산</button>
                <button class="mainspotbtn" @click="SelectArea('H')">세종</button>
                <button class="mainspotbtn" @click="SelectArea('I')">경기도</button>
                <button class="mainspotbtn" @click="SelectArea('J')">강원도</button>
                <button class="mainspotbtn" @click="SelectArea('K')">충청북도</button>
                <button class="mainspotbtn" @click="SelectArea('L')">충청남도</button>
                <button class="mainspotbtn" @click="SelectArea('M')">경상북도</button>
                <button class="mainspotbtn" @click="SelectArea('N')">경상남도</button>
                <button class="mainspotbtn" @click="SelectArea('O')">전라북도</button>
                <button class="mainspotbtn" @click="SelectArea('P')">전라남도</button>
                <button class="mainspotbtn" @click="SelectArea('Q')">제주도</button>
            </div>

            <div v-if="togetherSDs.length != 0">
              <v-col
                cols="12"
                sm="4"
                style="display:inline-block; padding:6px;"
                v-for="togetherSD in togetherSDs" :key="togetherSD.id"
              >
                <ScheduleCard :data="togetherSD.id" :schedule="togetherSD"/>
              </v-col>
            </div>

            <div v-else style="height: 21.75vw; padding-top: 10vw;"><h1 style="text-align: center;">해당하는 스케줄이 없습니다!</h1></div>
        </div>
        <div >
        </div>
      </div>
      <div>
        <div class="mb-3 mt-2">
            <h1 style="display:inline; color:#FF9617; font-size:2.7vw;">BEST</h1>
            <h3 style="display:inline; font-size:1.7vw;  ">여행지</h3>
            <!-- <button class="plusbtn">더보기</button> -->
        </div>
        <div v-for="bestma in bestmain" :key="bestma.id" style="display:inline;" >
            <!-- v-for -->
            <button class="besttag" >BEST</button>
            <SpotCard :spot="bestma" />
        </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/api'
import { mapGetters } from 'vuex'

import SpotCard from '@/components/spots/SpotCard';
import ScheduleCard from '@/components/schedules/ScheduleCard';

export default {
    components:{SpotCard,ScheduleCard},
    data () {
      return {
        bestmain:[],
        togetherSDs:[],
      }
    },
    computed: {
      ...mapGetters('accounts', ["LoginFlag", "config", "userInfo"]),
      headers() {
        return (this.LoginFlag ? {headers: {Authorization: this.config}} : null)
      },
    },
    methods: {
      getTogetherSD() {
        this.$http
        .get(process.env.VUE_APP_SERVER_URL +'/schedule', {
          params: {
            "together": 1
          }
        })
        .then(response => {
          this.togetherSDs = response.data.schedule.slice(0,3);
        })
        .catch(error => {
          console.log(error.response);
        })
      },
      SelectArea(area) {
         this.$http
        .get(process.env.VUE_APP_SERVER_URL +'/schedule', {
          params: {
            "area": area,
            "together": 1
          }
        })
        .then(response => {
          this.togetherSDs = response.data.schedule.slice(0,3);
        })
        .catch(error => {
          console.log(error.response);
        })
      },
      getBestSpots() {
        axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.BEST, this.headers)
        .then(res => {
          this.bestmain = res.data.slice(0,3);
        })
        .catch(error => {
          console.log(error.response);
          })
      }
    },
    created() {
      this.getTogetherSD();
      this.getBestSpots();
    }
  }
</script>

<style>
.maincenter {
    margin-top: 1%;
    width:66.6666666%;
    margin-left:16.6666666%;
}
.plusbtn {
    float:right;
    margin-top:18px;
    width:6%;
    font-size:1vw;
    height:2vw;
    border-radius:20px;
    background-color: #FF5E5E;
    color:white;
    outline:none;
    font-family: 'SCDream6'
}
.mainspotbtn {
    margin-right:6px;
    font-family: 'SCDream6';
    color:#707070;
    font-size:0.9vw;
}
.imo {
    font-family: 'SCDream5';
    font-size:0.9vw;
    color:#707070;
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