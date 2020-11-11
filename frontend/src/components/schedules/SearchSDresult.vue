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
          <h1 style="display:inline; color:#FF5E5E; font-size:2.7vw;">검색 결과</h1>
          <img src="@/assets/friend.png" style="margin-left: 8px;width:2%; height:1.2vw;" >
          <span class="imo"> 동행 모집</span>
          <img src="@/assets/help2.png" style="margin-left: 8px; width:2%; height:1.2vw;">
          <span class="imo"> 도움 요청</span>
        </div>
        <div>
          <v-col
            cols="12"
            sm="4"
            style="display:inline-block; padding:6px;"
            v-for="sche in schedules" :key="sche.id"
          >
          <ScheduleCard :data="sche.id" :schedule="sche" />
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
import ScheduleCard from '@/components/schedules/ScheduleCard';

import axios from 'axios'
import SERVER from '@/api/api'

export default {
  components:{ScheduleCard},
  data() {
    return {
      exschedule: 
        {
            "id": 0,
            "user": {
                "username": "",
                "nickname": "",
                "gender": "",
                "age": 0,
                "introduce": "",
                "profile_image": ""
            },
            "title": "",
            "overview": "",
            "private": 1,
            "advice": 1,
            "together": 1,
            "scrap_count": 0,
            "start_date": "",
            "end_date": "",
            "max_member": 0,
            "member_type_pk": 0,
            "style_type_pk": 0,
            "user_pk": 0,
            "coords": [[0, 0]],
            "avg_coord": [0, 0]
        },
        schedules:[],
        }
    },
    // computed: {
	// 	...mapGetters(["config","LoginFlag"]),
	// },
	// watch: {
	// 	page() {
	// 		this.getSpotList();}
	// },
	methods: {
		getScheduleList() {
			// pagination이랑 loginflag 해야함
      axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.SCHEDULES, {
        params: {
          title: this.$route.query.title,
          member_type: this.$route.query.member_type,
          style_type: this.$route.query.style_type,
          together: this.$route.query.together,
          advice: this.$route.query.advice,
          start_date: this.$route.query.start_date,
          end_date: this.$route.query.end_date,
        }
      })
      .then(response => {
        this.schedules = response.data.schedule
      })
      .catch(error => {
        console.log(error.response)
      })
		}
	},
	created(){
			this.getScheduleList();
		},
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
</style>