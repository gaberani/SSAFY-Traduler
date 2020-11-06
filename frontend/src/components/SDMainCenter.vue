<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col
        cols="12"
        sm="2"
      >
      </v-col>
      <v-col
        cols="12"
        sm="8"
      >
      <hr style=" background-color:#FF5E5E;">
      <div class="newSchedule">
        <div class="mb-3 mt-2">
          <h1 style="display:inline; color:#FF5E5E; font-size:2.7vw;">NEW</h1>
          <h3 style="display:inline; font-size:1.7vw;  "> 스케줄</h3>
          <img src="../assets/friend.png" style="margin-left: 8px;width:2%; height:1.2vw;" >
          <span class="imo"> 동행 모집</span>
          <img src="../assets/help2.png" style="margin-left: 8px; width:2%; height:1.2vw;">
          <span class="imo"> 도움 요청</span>
          <button class="plusbtn">더보기</button> 
        </div>
        <div>
          <v-col
            cols="12"
            sm="4"
            style="display:inline-block; padding:6px;"
            v-for="newSD in newschedules" :key="newSD.id"
          >
          <ScheduleCard :data="newSD.id*100000" :schedule="newSD" />
          </v-col>
        </div>
      </div>
      <div class="BESTSD">
        <div class="newSchedule mb-3 mt-2">
          <h1 style="display:inline; color:#FF9617; font-size:2.7vw;">BEST</h1>
          <h3 style="display:inline; font-size:1.7vw;  "> 스케줄</h3> 
        </div>
        <div>
          <!-------- 예시 -------------------------------------------------->
          <v-col
            cols="12"
            sm="4"
            style="display:inline-block; padding:6px;"
          >
          <button class="SDbesttag" >BEST</button>
          <ScheduleCard :data="1" :schedule="schedule"/>
          </v-col>
        </div>
      </div>
      <div class="HELPSD">
        <div class="newSchedule mb-3 mt-2">
          <h1 style="display:inline; color:#FF5E5E; font-size:2.7vw;">도움!</h1>
          <h3 style="display:inline; font-size:1.7vw;  "> 요청</h3> 
        </div>
        <div>
          <v-col
            cols="12"
            sm="4"
            style="display:inline-block; padding:6px;"
            v-for="helpSD in helpschedules" :key="helpSD.id"
          >
          <ScheduleCard :data="helpSD.id*1000" :schedule="helpSD"/>
          </v-col>
        </div>
      </div>
      </v-col>
      <v-col
        cols="12"
        sm="2"
      >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ScheduleCard from '@/components/ScheduleCard';
export default {
  components:{ScheduleCard},
  data() {
    return {
      schedule: 
        {
            "id": 38,
            "user": {
                "username": "Edgar3906",
                "nickname": "이동혁",
                "gender": "남성",
                "age": 28,
                "introduce": "",
                "profile_image": ""
            },
            "title": "서울 여행!",
            "overview": "주말동안 서울에 있는 관광 명소를 갈 생각이에요!!",
            "private": 1,
            "advice": 1,
            "together": 1,
            "scrap_count": 0,
            "start_date": "2020-11-06T18:00:00+09:00",
            "end_date": "2020-11-08T18:00:00+09:00",
            "max_member": 5,
            "member_type_pk": 4,
            "style_type_pk": 4,
            "user_pk": 24,
            "coords": [
                [37.5394, 127.065],
                [37.5348, 127.092],
                [37.6855, 127.073],
                [37.6855, 127.073],
                [37.5118, 127.059]
            ],
            "avg_coord": [
                37.567874999999994,
                127.07225
            ]
        },
        newschedules:[],
        bestschedules:[],
        helpschedules:[],
    }
  },
  methods: {
    getNewSD() {
      this.$http
      .get(process.env.VUE_APP_SERVER_URL +`/schedule/`)
      .then(response => {
      this.newschedules = response.data.schedule.reverse().slice(0,3)
      console.log(this.newschedules)
      })
      .catch(error => {
      console.log(error.response)
      })
    },
    getHelpSD() {
      this.$http
      .get(process.env.VUE_APP_SERVER_URL +`/schedule?title=`
      +`&member_type=&style_type=`
      +`&together=&advice=1`
      +`&start_date=&end_date=`)
      .then(response => {
      this.helpschedules = response.data.schedule.slice(0,3)
      // console.log(this.helpschedules)
      })
      .catch(error => {
      console.log(error.response)
      })
    }
  },
  created() {
    this.getNewSD();
    this.getHelpSD();
  }
}
</script>

<style>
.plusbtn {
    float:right;
    margin-top:2.5%;
    width:6%;
    font-size:1vw;
    height:2vw;
    border-radius:20px;
    background-color: #FF5E5E;
    color:white;
    outline:none;
    font-family: 'SCDream6'
}
.SDbesttag {
    z-index:10; 
    /* background-color:#FF9617;  */
    position:absolute; float:left; 
    transform: rotate(-45deg); 
    margin-left:-3%; 
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
.imo {
    font-family: 'SCDream5';
    font-size:0.9vw;
    color:#707070;
}
</style>