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
										<span v-else-if="schedule.style_type_pk===3" class="typefont">힐링</span>
										<span v-else class="typefont">힐링</span>
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
import SpotMap2 from '@/components/SpotMap2.vue'
import { mapGetters } from "vuex";
import moment from 'moment';
import 'moment/locale/ko'
export default {
    components: {SpotMap2},
    data() {
			return {
				schedule:[],
				SDdetail:{"course_coords": [
                [37.5394, 127.065],
                [37.5348, 127.092],
                [37.6855, 127.073],
                [37.6855, 127.073],
                [37.5118, 127.059]
            ],"avg_coord": [
                37.567874999999994,
                127.07225
            ]},
				SDcourse:[],
				advices:[],
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
			}
    },
    computed: {
		...mapGetters(["config","LoginFlag"]),
    },
    methods: {
			formatDate(date) {
				moment.locale('ko')
				const fmdate = moment(date).format('dddd, MM월 DD일')
				return{
						fmdate
				} 
			},
			formattime(time) {
				moment.locale('ko')
				const fmtime = moment(time).format('MM월 DD일 hh:mm')
				return{
						fmtime
				} 
			},
			getDetail() {
				const params = new URL(document.location).searchParams;
				this.$http
				.get(process.env.VUE_APP_SERVER_URL +`/schedule/${params.get('id')}`,{
						headers: {
								Authorization: this.config,
						},
				})
				.then(response => {
				this.schedule = response.data.schedule
				this.SDdetail = response.data
				this.SDcourse = response.data.course
				console.log(this.schedule)
				console.log(this.SDdetail)
				// 맵을 위해서 임시데이터   
				})
				.catch(error => {
				console.log(error.response)
				})
			}
    },
    created() {
			// /advice?schedule_pk={schedule_pk}&curPage={페이지}
			const params = new URL(document.location).searchParams;
			this.$http
			.get(process.env.VUE_APP_SERVER_URL +`/advice?schedule_pk=${params.get('id')}`,{
					headers: {
							Authorization: this.config,
					},
			})
			.then(response => {
				// console.log(response)
			console.log(response.data)
			this.advices = response.data.advice
			// 맵을 위해서 임시데이터   
			})
			.catch(error => {
			console.log(error.response)
			})
			this.getDetail()
		}
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