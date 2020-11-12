<template>
  <v-app>
    <v-row no-gutters style="max-height:650px;">
      <v-col
        cols="12"
        sm="3"
        class=""
        style="margin-top:25px;"
      >
        <center>
					<h1 style="font-size:2.2vw;">{{schedule.title}}</h1>
					<button class="sharebtn" @click.prevent="ScrapSchedule"><i class="fas fa-share" style="font-size:1.3vw; color:white"></i></button>
          <!-- <button v-if="schedule.together===1" class="togetherbtn" v-bind="attrs" v-on="on">동행 신청</button> -->
          <v-dialog
            v-model="dialog"
            max-width="500"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="rgba( 13, 136, 255)"
                class="togetherbtn"
                v-bind="attrs"
                v-on="on"
              >
                동행 신청
              </v-btn>
            </template>
            <v-card>
              <v-card-title class="headline" >
                <img src="@/assets/friend.png" style="width:7%; height:1.6rem;" >
                <span style="font-family: 'SCDream5';font-size:1.5rem;">
                  
                  동행 신청
                </span>
              </v-card-title>
              <center>
                <v-text-field
                  v-model="joincontent"
                  label="신청메시지"
                  style="font-family: 'SCDream5'; width:95%;"
                  placeholder="신청과 함께 보내고 싶은 메시지를 입력해주세요."
                  outlined
                  dense
                  hide-details
                ></v-text-field>
              </center>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="#FF5E5E"
                  text
                  style="font-family: 'SCDream4'"
                  @click="dialog = false"
                >
                  취소
                </v-btn>
                <v-btn
                  color="rgba( 13, 136, 255)"
                  text
                  style="font-family: 'SCDream4'"
                  @click="JoinSchedule"
                >
                  신청하기
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
					<div class="inf">
						<span style="font-family: 'SCDream5';font-size:1.2vw;">
							{{formatDate(schedule.start_date)}} - {{formatDate(schedule.end_date)}}
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
									<div v-if="schedule.together===1"  style="margin-top:0.6vw">
										<img src="@/assets/friend.png" style="width:20%; height:1.3vw;" >
										<span class="imo"> 동행 모집</span>
									</div> 
									<div v-if="schedule.advice===1"  style="margin-top:0.6vw">
										<img src="@/assets/help2.png" style="width:20%; height:1.3vw;">
										<span class="imo"> 도움 요청</span>
									</div>
                  <div v-if="schedule.together===0"  style="margin-top:0.6vw;height:1.3vw;">
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
									<span class="spottime">{{formattime(cour.start_time)}} ~ {{formattime(cour.end_time)}}</span>
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
							<h3 style="font-size:2vw; color:#FF5E5E">도움 게시판</h3>
              <div v-if="advices.length===0" class="onecomment">
                <p style="margin-top:10px;font-size:1vw;"> 등록된 게시글이 없습니다.</p>
              </div>
            </center>
						<div class="onecomment" v-for="(ad,index) in advices" :key="ad.id">
							<p style="margin-top:10px;margin-left:8px;margin-bottom:5px; font-size:1vw;" >
								<img class="helpperson" v-if="ad.user.gender==='여성'" src="@/assets/girl.png">  
								<img class="helpperson" v-else src="@/assets/boy.png">
								{{ad.content}}
                <button @click="deleteComment(ad.id,index)" v-if="username == ad.user.username"><i class="far fa-times-circle" style="color:red;"></i></button> 
								<span style="font-size:0.9vw;font-family: 'SCDream3'; color:#F707070;"> - {{ad.user.nickname}}</span>
							</p>
						</div>
            <div v-if="advicepage.endPage>1" class="text-center">
              <v-pagination
                v-model="page"
                :length="advicepage.endPage"
                :total-visible="3"
                circle
              ></v-pagination>
            </div>
            <center>
              <v-text-field class="commentinput" v-model="writecomment" hide-details placeholder="글을 작성해주세요."></v-text-field>
              <button @click.prevent="WriteComment" class="commentinputbtn">작성</button>
              <!-- <i class="fas fa-pen"></i> -->
            </center>
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
      joincontent:'',
      dialog:false,
      schedule: [],
      writecomment:'',
      page:1,
      advicepage:[],
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
    ...mapGetters(["config", "LoginFlag", "userInfo"]),
    headers() {
      return (this.LoginFlag ? {Authorization: this.config} : null)
    },
    username() {
      return sessionStorage.getItem("username");
    },
  },
  watch: {
      page() {
        axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.ADVICE, {
          headers: this.headers,
          params: {
            schedule_pk: this.$route.params.schedule_id,
            curPage:this.page
          }
        })
        .then(response => {
          this.advices = response.data.advice;
        })
        .catch(error => console.log(error))
      }
    },
  methods: {
    JoinSchedule() {
        let joinbody = {
          schedule_pk: this.$route.params.schedule_id,
          content: this.joincontent
        }
        axios.post(process.env.VUE_APP_SERVER_URL + '/join/', joinbody, {
            headers: this.headers,
          })
          .then(response => {
            console.log(response)
            this.joincontent = '';
            this.dialog = false;
            alert("동행 신청이 되었습니다!!");
          })
          .catch(error => { 
            console.log(error)
            alert("동행 신청 실패")
          })
    },
    ScrapSchedule() {
      let res = confirm('스크랩 하시겠습니까?')
        if (res) {
          let scrapbody = {
            schedule_pk: this.$route.params.schedule_id,
          }
          axios.post(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.SCHEDULES+'scrap/', scrapbody, {
            headers: this.headers
          }
          )
          .then(response => {
            console.log(response)
            alert("스크랩되었습니다!!");
          })
          .catch(error => {
            console.log(error.response)
            alert("스크랩실패..");
          })
        }
    },
    WriteComment() {
      if (this.writecomment.length >33) {
        alert("33자 이내로 입력해주세요.");
      } else {
      let body = {
        schedule_pk: this.$route.params.schedule_id,
        content: this.writecomment
      }
      axios.post(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.ADVICE, body, {
        headers: this.headers
      }
      )
      .then(response => {
        this.advices.unshift(response.data);
        this.writecomment="";
      })
      .catch(error => {
        console.log(error.response)
      })}
    },
    deleteComment(commentid, index) {
      axios.delete(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.ADVICE + commentid,{
        headers: this.headers
      })
      .then(() => {
        this.advices.splice(index,1);
      })
      .catch(err => console.log(err.response))
    },
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
        console.log(this.SDdetail)
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
        this.advicepage = response.data.page;
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
    /* margin-left:3%; */
    width:20%;
    height:35px;
    border-radius:3px;
    background-color:#FF5E5E;
    margin-top:2px;
}
.togetherbtn {
    margin-left:3%;
    /* height:25px; */
    width:20%;
    color:white;
    /* border-radius:3px; */
    /* background-color:rgba( 13, 136, 255); */
    font-family: 'SCDream6';
    font-size:1vw;
}
.inf {
    margin-top:10px;
    border-top:4px #FF5E5E solid;
    border-bottom:4px #FF5E5E solid;
		border-radius:10px;
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
/* 스크롤 바 넓이 16px */
.courseinf::-webkit-scrollbar{width: 16px;}
/* 스크롤 바 기본 색상 */
.courseinf::-webkit-scrollbar-track {background-color:#FF5E5E;
    box-shadow: inset 0px 0px 5px white;
    border-radius: 10px;
}
/* 스크롤 구간 배경 색상 */
.courseinf::-webkit-scrollbar-thumb {background-color:#ff9a9a;
    border-radius: 10px;
} 
/* 스크롤 바 위에 마우스 올렸을 때(hover) 색상 */
.courseinf::-webkit-scrollbar-thumb:hover {background-color: #fd4b4b;} 
.helptable {
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
    font-size:1.3vw;
}
.spottime {
    font-family: 'SCDream4';
    font-size:1vw;
    color:#707070;
    display: block;
    margin-bottom: 5px;
}
.courseidx {
    width:27px;
    height:27px;
    margin-left:5px;
    margin-right:5px;
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
.helpperson {
	width:1.2vw;
}
.onecomment {
	border:5px #707070 double;
	min-height: 3.5vw;
	margin-top:2%;
	border-radius:10px;
}
.commentinputbtn {
  margin-top:3px;
  font-family: 'SCDream3';
  font-size:1vw;
  float:right;
  color:white;
  background-color:#FF5E5E;
  width:5vw;
  margin-right:5px;
  border-radius:3px;
}
.commentinput {
  font-size:0.9vw;
  font-family: 'SCDream4'; 
  width:95%;
}
</style>