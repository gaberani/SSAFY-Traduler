<template>
  <v-app>
    <v-row no-gutters style="max-height:650px;">
      <v-col
        cols="12"
        sm="3"
        class=""
        style="margin-top:25px; border-right:3px #FF5E5E solid;"
      >
        <center>
					<h1 style="font-size:2.1vw; display:inline;">{{schedule.title}}</h1>
					<button class="sharebtn"><i class="fas fa-share" style="color:white"></i></button>
					<div class="inf">
						<span style="font-family: 'SCDream5';font-size:1.2vw;">
							{{formatDate(schedule.start_date).fmdate}} - {{formatDate(schedule.end_date).fmdate}}
						</span>
						<v-row no-gutters class="SDinf">
								<v-col
									cols="12"
									sm="4"
									style="border-right:1px #707070 solid;"
								> 
									<div style="margin-top:1.2vw;">
										<span v-if="schedule.member_type_pk===1" class="typefont">혼자</span>
										<span v-else-if="schedule.member_type_pk===2" class="typefont">가족</span>
										<span v-else-if="schedule.member_type_pk===3" class="typefont">커플</span>
										<span v-else class="typefont">3인이상</span>
									</div>
								</v-col>
								<v-col
									cols="12"
									sm="4"
									style="border-right:1px #707070 solid;"
								> 
									<div style="margin-top:1.2vw;">
										<span v-if="schedule.style_type_pk===1" class="typefont">힐링</span>
										<span v-else-if="schedule.style_type_pk===2" class="typefont">액티비티</span>
										<span v-else-if="schedule.style_type_pk===3" class="typefont">맛집 탐방</span>
										<span v-else class="typefont">역사 탐방</span>
									</div>
								</v-col>
								<v-col
									cols="12"
									sm="4"
								> 
									<div style="margin-top:0.6vw">
										<img src="@/assets/friend.png" style="width:20%; height:1.3vw;" >
										<span class="imo"> 동행 모집</span>
									</div>    
									<div style="margin-top:0.6vw">
										<img src="@/assets/help2.png" style="width:20%; height:1.3vw;">
										<span class="imo"> 도움 요청</span>
									</div>    
								</v-col>
						</v-row>
					</div>
					</center>
					<div class="courseinf">
						<v-col
							cols="12"
							sm="1"
						>     
						</v-col>
							<v-col
								cols="12"
								sm="11"
							>     
							<i class="fas fa-flag" style="font-size:2rem;"></i>
							<div style="width:90%; margin-left:1%; border-left:3.3px black solid">
								<div v-for="(cour,idx) in SDcourse" :key="cour.id">
									<p v-if="idx!=0" style="font-size:1.6rem; margin-left:-15px; margin-bottom:5px;"><i class="fas fa-car"></i></p>
									<button class="courseidx" style="background-color:">{{idx+1}}</button>
									<span class="spottitle">{{cour.spot_info.title}}</span>
									<span class="spottime">{{formattime(cour.start_time).fmtime}} ~ {{formattime(cour.end_time).fmtime}}</span>
								</div>
							</div>
							<i class="fas fa-check-circle car" style="font-size:2rem; color:blue;"></i>
						</v-col>
					</div>
        </v-col>
        <v-col
					cols="12"
					sm="7"
					style="margin-top:25px;"
        >
        <SpotMap2 :item="schedule.id" :SDdetail="SDdetail" class="cardmap"></SpotMap2>
        </v-col>
        <v-col
					cols="12"
					sm="2"
        > 
					<div class="helptable">
						<center>
							<h3 style="margin-top:10px; font-size:1.3vw;">도움 게시판</h3>
							<p v-if="advices.length===0" style="margin-top:10px;font-size:1vw;"> 등록된 게시글이 없습니다.</p>
						</center>
						<p style="margin-top:10px;margin-left:8px;margin-bottom:5px; font-size:1.3vw;" v-for="ad in advices" :key="ad.id"><i class="fas fa-circle"></i>  {{ad.content}} - {{ad.user.nickname}}</p>
					</div>    
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col
					cols="12"
					sm="3"
        >
        </v-col>
        <v-col
					cols="12"
					sm="7"
        >
        </v-col>
        <v-col
					cols="12"
					sm="2"
        > 
        </v-col>
      </v-row>
  </v-app>
</template>

<script>
import SpotMap2 from '@/components/schedules/SpotMap2.vue'

import { mapGetters } from "vuex";
import SERVER from '@/api/api'
import axios from 'axios'

import moment from 'moment';
import 'moment/locale/ko'

export default {
  components: {
    SpotMap2
  },
  data() {
    return {
      schedule: [],
      SDdetail: {
        "course": [
          {
            "id": 0,
            "spot_info": {
              "id": 0,
              "is_liked": false,
              "title": "",
              "overview": "",
              "lon": 0,
              "lat": 0,
              "tel": null,
              "tel_name": null,
              "image": "",
              "address": "",
              "content_type_pk": 0,
              "area_code": "",
              "category_code": ""
            },
            "custom_spot_info": null,
            "memos": [],
            "start_time": "",
            "end_time": "",
            "content": "",
            "budget_food": 0,
            "budget_transport": 0,
            "budget_entrance": 0,
            "budget_room": 0,
            "budget_etc": 0,
            "schedule_pk": 0,
            "spot_pk": 0,
            "custom_spot_pk": null,
            "user_pk": 0
          },
        ],
        "course_coords": [[0, 0]],
        "avg_coord": [0, 0]
      },
      SDcourse: [],
      advices: [],
      exschedule: {
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
        "private": 0,
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
    }
  },
  computed: {
    ...mapGetters(["config", "LoginFlag"]),
    headers() {
      return (this.LoginFlag ? {Authorization: this.config} : null)
    },
    
  },
  methods: {
    formatDate(date) {
      moment.locale('ko');
      return moment(date).format('dddd, MM월 DD일')
    },
    formattime(time) {
      moment.locale('ko');
      return moment(time).format('MM월 DD일 hh:mm')
    },
    getDetail() {
      axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.SCHEDULES + this.$route.params.schedule_id, {
        headers: this.headers
      })
      .then(response => {
        this.SDdetail = response.data;
        this.schedule = response.data.schedule;
        this.SDcourse = response.data.course;
      })
      .catch(error => {
        console.log(error.response)
      })
    },
    getAdvice() {
      axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.ADVICE, {
        headers: this.headers,
        params: {
          schedule_pk: this.$route.params.schedule_id
        }
      })
      .then(response => {
        this.advices = response.data.advice;
      })
      .catch(error => {
        console.log(error.response);
      })
    }
  },
  created() {
    this.getDetail();
    this.getAdvice();
  },
  }
</script>

<style scoped>
.sharebtn {
    margin-left:8%;
    width:10%;
    border-radius:3px;
    background-color:#FF5E5E;
}
.inf {
    margin-top:10px;
    border-top:3px #FF5E5E solid;
    border-bottom:3px #FF5E5E solid;
    width: 90%;
    /* height: 100px;  */
}
.SDinf {
    /* height: 70px; */
}
.typefont {
    font-family: 'SCDream6';
    font-size:1.2vw;
}
.imo {
    font-family: 'SCDream6';
    font-size:1vw;
}
.courseinf {
    /* margin-top: 1px; */
    /* margin-left: 20px; */
    height:500px;
    overflow-y: auto;
    /* width:90%; */
}
.helptable {
    border: 5px #FF5E5E solid;
		right:1.5%;
    top:10%;
    /* width: 15%; */
    width:15vw;
    height:600px;
    border-radius:30px;
    margin-top:20px;
    position: fixed;
}
.spottitle {
    font-family: 'SCDream4';
    font-size:1.5vw;
}
.spottime {
    font-family: 'SCDream4';
    font-size:1vw;
    color:#707070;
    display: block;
    margin-bottom: 5px;
}
.courseidx {
    width:25px;
    background-color:#FF5E5E;
    color:white;
    border-radius:100%;
    /* margin-left:-6%; */
}
.courseidx:hover {
    background-color:#850b0b;
}
.car {
    margin-left:-12px;
    margin-top:-6px;
}
</style>