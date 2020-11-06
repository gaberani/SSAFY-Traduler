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
          <img src="../assets/friend.png" style="margin-left: 8px;width:2%; height:1.2vw;" >
          <span class="imo"> 동행 모집</span>
          <img src="../assets/help2.png" style="margin-left: 8px; width:2%; height:1.2vw;">
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
import ScheduleCard from '@/components/ScheduleCard';
export default {
  components:{ScheduleCard},
  data() {
    return {
      exschedule: 
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
        // page:1,
        schedules:[],
        // SDspage:[],
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
		getSDList() {
			// pagination이랑 loginflag 해야함
            const params = new URL(document.location).searchParams;
            this.$http
            .get(process.env.VUE_APP_SERVER_URL +`/schedule?title=${params.get('title')}`
            +`&member_type=${params.get('member_type')}&style_type=${params.get('style_type')}`
            +`&together=${params.get('together')}&advice=${params.get('advice')}`
            +`&start_date=${params.get('start_date')}&end_date=${params.get('end_date')}`)
            .then(response => {
            this.schedules = response.data.schedule
            console.log(this.schedules)
            })
            .catch(error => {
            console.log(error.response)
            })
		}
	},
	created(){
			this.getSDList();
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