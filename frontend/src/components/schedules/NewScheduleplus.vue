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
      <div class="text-center">
        <v-pagination
          v-model="curPage"
          :length="schedulespage.endPage"
          :total-visible="7"
          class="mt-5"
        ></v-pagination>
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
import { mapGetters } from "vuex";
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
        schedulespage:[],
        curPage:1,
        }
    },
  watch: {
    curPage() {
      this.movePage();
    }
  },
  computed: {
      ...mapGetters('accounts', ["config", "LoginFlag"]),
      headers() {
        return (this.LoginFlag ? {Authorization: this.config} : null)
      },
    },
	methods: {
    movePage() {
        this.$router.push({ query: {
          curPage: this.curPage
          }
        }).catch(()=>{})
      },
		getNewSchedule() {
      axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.SCHEDULES, {
          headers: this.headers
        })
      .then(response => {
        this.schedules= response.data.schedule;
        this.schedulespage=response.data.page;
      })
      .catch(error => {
        console.log(error.response);
      })
        }
	},
	created(){
      this.getNewSchedule();
      this.curPage = this.$route.query.curPage * 1
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