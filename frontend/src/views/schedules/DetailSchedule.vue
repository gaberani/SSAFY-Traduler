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
            v-if="schedule.together===1 && username != schedule.user.username"
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
          <v-dialog
              v-model="editdialog"
              max-width="500"
              v-if="username == schedule.user.username"
          >
            <template v-slot:activator="{ on, attrs }">
              <button 
                style="font-size:1.5vw; float:right; margin-right:5%; color:green;"
                v-bind="attrs"
                v-on="on"
              >
                <i class="fas fa-cog"></i>
              </button>
            </template>
            <v-card>
            <v-card-title class="headline" >
              <span style="font-family: 'SCDream5';font-size:1.5rem; margin-bottom:5px;">
            
              스케줄 수정/삭제
              </span>
            </v-card-title>
            <center>
              <v-text-field
                dense
                label="스케줄 제목"
                style="width:80%; font-size:1.5vw; font-family: 'SCDream6'; border:'#FF5E5E'"
                v-model="edittitle"
              ></v-text-field>
              <v-text-field
                dense
                label="스케줄 Overview"
                style="width:90%; font-size:1.2vw; font-family: 'SCDream5'; "
                v-model="editoverview"
              ></v-text-field>
              <v-select
                :items="member"
                label="멤버 타입"
                class="memtypeselect"
                v-model="editmember_type"
              ></v-select>
              <v-select
                :items="type"
                label="컨셉"
                class="memtypeselect"
                style="margin-left:5px;"
                v-model="edittravel_type"
              ></v-select>
              <v-text-field
                dense
                type="number"
                label="참여 인원(명)"
                placeholder="숫자로 입력해주세요."
                style="width:25%; font-size:1vw; font-family: 'SCDream5'; "
                v-model="editmax_member"
                hide-details
              ></v-text-field>
              <v-menu
                  v-model="editmenu2"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  width="50%"
                  >
                  <template v-slot:activator="{ on, attrs }" >
                      <v-text-field
                      v-model="editstartdate"
                      placeholder="가는날 (이후)"
                      prepend-icon="mdi-car"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      hide-details
                      style="width:50%; font-family: 'SCDream5'; "
                      ></v-text-field>
                  </template>
                  <v-date-picker
                      v-model="editstartdate"
                      @input="editmenu2 = false"
                  ></v-date-picker>
              </v-menu>
              <v-menu
                v-model="editmenu3"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                >
                <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                    v-model="editenddate"
                    placeholder="오는날 (이전)"
                    prepend-icon="mdi-home"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    style="width:50%; font-family: 'SCDream5';"
                    ></v-text-field>
                </template>
                <v-date-picker
                    v-model="editenddate"
                    @input="editmenu3 = false"
                ></v-date-picker>
            </v-menu>
              <v-row no-gutters >
                <v-col
                  cols="12"
                  sm="6"
                >
                  <div style="font-family: 'SCDream5'; font-size:1.3vw;">
                    <span style="margin-right:2px;">공개</span><input type="radio" name="private" v-model="privatebtn" value="0">
                  </div>
                  <div v-if="privatebtn=='0'">
                    <img src="@/assets/friend.png" style="width:5%; height:1.1vw;" ><span style="margin-right:2px;font-family: 'SCDream4';font-size:1.1vw;">동행 모집</span>
                    <input type="checkbox" v-model="edittogether">
                  </div>
                  <div v-else>
                    <img src="@/assets/friend.png" style="width:5%; height:1.1vw;" ><span style="margin-right:2px;font-family: 'SCDream4';font-size:1.1vw;">동행 모집</span>
                    <input disabled type="checkbox" v-model="edittogether">
                  </div>
                  <div v-if="privatebtn=='0'">
                    <img src="@/assets/help2.png" style="width:5%; height:1.1vw;"><span style="margin-right:2px;font-family: 'SCDream4';font-size:1.1vw;">도움 요청</span>
                    <input type="checkbox" v-model="editadvice">
                  </div>
                  <div v-else>
                    <img src="@/assets/help2.png" style="width:5%; height:1.1vw;"><span style="margin-right:2px;font-family: 'SCDream4';font-size:1.1vw;">도움 요청</span>
                    <input disabled type="checkbox" v-model="editadvice">
                  </div>
                </v-col>
                <v-col
                  cols="12"
                  sm="6"
                  style="border-left:2px #707070 solid;"
                >
                  <div style="font-family: 'SCDream5'; font-size:1.3vw;">
                    <span style="margin-right:2px;">비공개</span><input type="radio" name="private" v-model="privatebtn" value="1">
                  </div>
                </v-col>
              </v-row>
            </center>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                color="#FF5E5E"
                text
                style="font-family: 'SCDream6'; border:2px #FF5E5E solid; margin-right:220px;"
                @click="deleteSchedule"
                >
                스케줄 삭제
                </v-btn>
                <v-btn
                color="#FF5E5E"
                text
                style="font-family: 'SCDream4'"
                @click="editdialog = false"
                >
                취소
                </v-btn>
                <v-btn
                color="rgba( 13, 136, 255)"
                text
                style="font-family: 'SCDream4'"
                @click="editScheduler"
                >
                수정
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
                style="padding-right:0;"
							>     
							<i class="fas fa-flag" style="font-size:2rem;"></i>
              <v-dialog
                v-model="dialog2"
                max-width="300"
                v-if="username == schedule.user.username">
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="courseplusbtn"
                    v-bind="attrs"
                    v-on="on"
                  >
                    코스 추가
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title class="headline" >
                    <span style="font-family: 'SCDream5';font-size:1.5rem;">
                      
                      코스 추가
                    </span>
                  </v-card-title>
                  <center>
                    <!-- <v-select
                      style="font-family: 'SCDream5';font-size:1.3rem; width:80%;"
                      :items="selectarea"
                      label="지역 선택"
                      dense
                    ></v-select> -->
                    <multiselect class="spotselect" :optionsLimit='5' 
                      v-model="spot2" 
                      :options="spots2" 
                      :custom-label="spotWithTitle" placeholder="여행지 검색" label="name" track-by="name"></multiselect>
                    <!-- <v-select
                      style="font-family: 'SCDream5';font-size:1.1rem; width:50%;"
                      :items="selectarea"
                      label="여행지 선택"
                      dense
                      hide-details
                    ></v-select> -->
                    <v-menu
                      v-model="menu2"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      transition="scale-transition"
                      offset-y
                      width="50%"
                      >
                      <template v-slot:activator="{ on, attrs }" >
                          <v-text-field
                          v-model="startdate"
                          placeholder="가는날 (이후)"
                          prepend-icon="mdi-car"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                          
                          style="width:50%; font-family: 'SCDream5';"
                          ></v-text-field>
                      </template>
                      <v-date-picker
                          v-model="startdate"
                          @input="menu2 = false"
                      ></v-date-picker>
                  </v-menu>
                  
                  <v-select
                    v-model="DdepartureHour"
                    :items="DHours"
                    menu-props="auto"
                    label="출발(시)"
                    outlined
                    dense
                    hide-details
                    style="width:40%;display:inline-block; font-family: 'SCDream4';"
                  ></v-select>
                
                  <v-select
                    v-model="DdepartureMinute"
                    :items="DMinutes"
                    menu-props="auto"
                    label="출발(분)"
                    outlined
                    dense
                    hide-details
                    style="width:40%; margin-left:10px; display:inline-block; font-family: 'SCDream4';"
                  ></v-select>							
                  <v-menu
                      v-model="menu3"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      transition="scale-transition"
                      offset-y
                      >
                      <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                          v-model="enddate"
                          placeholder="오는날 (이전)"
                          prepend-icon="mdi-home"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                          style="width:50%; font-family: 'SCDream5';"
                          ></v-text-field>
                      </template>
                      <v-date-picker
                          v-model="enddate"
                          @input="menu3 = false"
                      ></v-date-picker>
                  </v-menu>
                  <v-select
                    v-model="DarrivalHour"
                    :items="DHours"
                    menu-props="auto"
                    label="도착(시)"
                    outlined
                    dense
                    hide-details
                    style="width:40%;display:inline-block;font-family: 'SCDream4';"
                  ></v-select>
                
                  <v-select
                    v-model="DarrivalMinute"
                    :items="DMinutes"
                    menu-props="auto"
                    label="도착(분)"
                    outlined
                    dense
                    hide-details
                    style="width:40%;display:inline-block; margin-left:10px;font-family: 'SCDream4';"
                  ></v-select>
                  </center>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="#FF5E5E"
                      text
                      style="font-family: 'SCDream4'"
                      @click="dialog2 = false"
                    >
                      취소
                    </v-btn>
                    <v-btn
                      color="rgba( 13, 136, 255)"
                      text
                      style="font-family: 'SCDream4'"
                      @click="schedulePlus"
                    >
                      추가하기
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
							<div style="width:90%; margin-left:1%; border-left:3.3px black solid; margin-top:3px;">
								<div v-for="(cour,idx) in SDcourse" :key="cour.id">
									<p v-if="idx!=0" style="font-size:1.6rem; margin-left:-15px; margin-bottom:5px;"><i class="fas fa-car"></i></p>
									<button class="courseidx" style="background-color:">{{idx+1}}</button>
									<span class="spottitle">{{cour.spot_info.title}}</span>
                  <button v-if="username == schedule.user.username" @click="deletecourse(cour.id,idx)" style="float:right; font-size:2rem; color:green; font-family: 'SCDream6';">-</button>
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
          <div v-if="schedule.advice==0" class="helptable">
						<center>
							<h3 style="font-size:2vw; color:#FF5E5E">도움 게시판</h3>
              <div v-if="advices.length===0" class="onecomment">
                <p style="margin-top:10px;font-size:1.3vw;"> 도움 요청이 비활성화된 스케줄입니다.</p>
              </div>
            </center>
          </div>
					<div v-else class="helptable">
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
      <v-row style="margin-top:80px;" no-gutters>
        <v-col
					cols="12"
					sm="10"
        >
        <center>
          <DetailCalendar :Courses="SDcourse" />
        </center>
        </v-col>
        <v-col
					cols="12"
					sm="3"
        > 
        </v-col>
      </v-row>
  </v-app>
</template>

<script>
import SpotMap2 from '@/components/schedules/SpotMap2.vue'
import DetailCalendar from '@/components/schedules/DetailCalendar.vue'
import { mapGetters } from "vuex";
import SERVER from '@/api/api'
import axios from 'axios'
import Multiselect from 'vue-multiselect'
import moment from 'moment';
import 'moment/locale/ko'

export default {
  components: {
    SpotMap2,
    DetailCalendar,
    Multiselect
  },
  data() {
    return {
      schedule: {"user": {
          "username": "",
          "nickname": "",
          "gender": "",
          "age": 0,
          "introduce": "",
          "profile_image": ""
        },},
      // 수정
      edittitle:'',
      editoverview:'',
      editdialog:false,
      privatebtn:"1",
      edittogether:false,
      editadvice:false,
      editmember_type:'',
      edittravel_type:'',
      editstartdate: '',
      editenddate: '',
      editmax_member:1,
      editmenu3: false,
      editmenu2: false,
      member : ['혼자','가족','커플','3인이상'],
      type : ['힐링','액티비티','맛집 탐방','역사 탐방'],
      formatstartdate:'',
      formatenddate:'',
      // 
      // 코스 추가
      spot2:'',
			spots2:[],
      dialog2:false,
      startdate: '',
      enddate: '',
      menu3: false,
      menu2: false,
      createcourse: [],
      custom_spot_pk:null,
      // 출발, 도착 시간 변수
      DHours: [...Array(24)].map((v,i) => i+1),
      DMinutes: [...Array(4)].map((v,i) => i*15),
      DdepartureHour: null,
      DdepartureMinute: '00',
      DarrivalHour: null,
			DarrivalMinute: '00',
			coursestarttime:'',
			courseendtime:'',
      // 
      joincontent:'',
      dialog:false,
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
    deleteSchedule() {
      let res = confirm('스케줄을 삭제 하시겠습니까?')
      if (res) {
        axios.delete(process.env.VUE_APP_SERVER_URL +  SERVER.URL.SCHEDULE.SCHEDULES +this.$route.params.schedule_id, {
            headers: {
              Authorization : this.config,
        }})
        .then(response => {
          console.log(response)
          alert("스케줄을 삭제하였습니다.")
          this.$router.push({name: 'Home'})
        })
        .catch(error => { 
          console.log(error.response)
        })}
    },
    editScheduler() {
      if (this.edittitle.length !=0 && this.editoverview.length !=0 && this.editstartdate.length !=0 &&
				this.editenddate.length !=0 ) {
				this.formatstartdate = this.editstartdate + 'T00:00:00+09:00'
				this.formatenddate = this.editenddate + 'T23:59:00+09:00'
				let editbody = {
					title : this.edittitle,
					overview :this.editoverview,
					private : this.privatebtn,
					advice : this.editadvice*1,
					together : this.edittogether*1,
					member_type_pk: this.changeMemtype(),
					style_type_pk: this.changeStyletype(),
					start_date: this.formatstartdate,
					end_date: this.formatenddate,
					max_member: this.editmax_member,
        }
        axios.patch(process.env.VUE_APP_SERVER_URL +  SERVER.URL.SCHEDULE.SCHEDULES +this.$route.params.schedule_id+'/', editbody, {
            headers: {
							Authorization : this.config,
				}})
				.then(response => {
					console.log(response)
          alert("스케줄을 수정하였습니다.")
          this.schedule.title = response.data.title
          this.schedule.overview = response.data.overview
          this.schedule.private = response.data.private
          this.schedule.advice = response.data.advice
          this.schedule.together = response.data.together
          this.schedule.member_type_pk = response.data.member_type_pk
          this.schedule.style_type_pk = response.data.style_type_pk
          this.schedule.start_date = response.data.start_date
          this.schedule.end_date =response.data.end_date
          this.schedule.max_member = response.data.max_member
          this.editdialog =false
				})
				.catch(error => { 
					console.log(error.response)
				})} else {
					alert("빈칸을 채워주세요!!")
				}
    },
    changeMemtype() {
			return this.member.indexOf(this.editmember_type) +1
			},
		changeStyletype() {
			return this.type.indexOf(this.edittravel_type) +1
		},
    deletecourse(id,index) {
      let res = confirm('코스를 삭제 하시겠습니까?')
      if (res) {
        axios.delete(process.env.VUE_APP_SERVER_URL + `/course/` + id,{
          headers: this.headers
        })
        .then(() => {
          this.SDcourse.splice(index,1);
          this.SDdetail.course_coords.splice(index,1);
        })
        .catch(err => console.log(err.response))
      }
    },
    spotWithTitle({title}) {
			return `${title}`
		},
		schedulePlus() {
			console.log(this.DdepartureHour.length)
			if (this.spot2 && this.startdate && this.DdepartureHour &&
			this.enddate && this.DarrivalHour ) {
				if (this.DdepartureHour < 10) {
					this.DdepartureHour = '0'+this.DdepartureHour
				}
				if (this.DarrivalHour < 10) {
					this.DarrivalHour = '0'+this.DarrivalHour
				}
				if (this.DdepartureMinute.length == 1) {
					this.DdepartureMinute = '0'+this.DdepartureMinute
				}
				if (this.DarrivalMinute.length == 1) {
					this.DarrivalMinute = '0'+this.DarrivalMinute
        }
        var d1 = new Date(this.startdate)
        var d2 = new Date(this.schedule.start_date)
        var d3 = new Date(this.enddate)
        var d4 = new Date(this.schedule.end_date)
        if (d1 >= d2 && d4 >= d3) {
        console.log(this.DdepartureHour)
        this.schedulePlusunit()
      } else {
        alert("스케줄 날짜와 코스 날짜를 확인해주세요.")
      }
			} 
		},
		schedulePlusunit() {
			this.coursestarttime = this.startdate + 'T' +this.DdepartureHour +':'+this.DdepartureMinute+':00+09:00'
			this.courseendtime = this.enddate + 'T' +this.DarrivalHour +':'+this.DarrivalMinute+':00+09:00'
       let coursebody = {
        schedule_pk: this.$route.params.schedule_id,
        spot_pk: this.spot2.id,
        content: "test",
        start_time : this.coursestarttime,
        end_time : this.courseendtime,
        custom_spot_pk : this.custom_spot_pk
      }
      axios.post(process.env.VUE_APP_SERVER_URL + '/course/', coursebody, {
          headers: this.headers,
        })
        .then(response => {
          console.log(response)
          this.SDdetail.course_coords.push([
            response.data.spot_info.lat,response.data.spot_info.lon
          ])
          this.SDcourse.push({
            'spot_info' : { 
              'title':this.spot2.title
            },
            'spot_pk':this.spot2.id,
            'start_time' : this.coursestarttime,
            'end_time' : this.courseendtime,
          })
        })
        .catch(error => { 
          console.log(error.response)
        })
			console.log(this.createcourse)
			console.log(this.spot2.title)
			console.log(this.coursestarttime)
			console.log(this.courseendtime)
			this.dialog2 = false
		},
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
    formatEditDate(date) {
      moment.locale('ko');
      return moment(date).format('yyyy-MM-DD')
    },
    formattime(time) {
      moment.locale('ko');
      return moment(time).format('MM월 DD일 a hh:mm')
    },
    getDetail() {
      axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.SCHEDULES + this.$route.params.schedule_id, {
        headers: this.headers
      })
      .then(response => {
        this.SDdetail = response.data;
        this.schedule = response.data.schedule;
        this.SDcourse = response.data.course;
        // 수정데이터
        this.edittitle = this.schedule.title
        this.editoverview = this.schedule.overview
        this.privatebtn =this.schedule.private
        this.edittogether= this.schedule.together,
        this.editadvice= this.schedule.advice
        this.editmember_type = this.member[this.schedule.member_type_pk-1]
        this.edittravel_type = this.type[this.schedule.style_type_pk-1]
        this.editstartdate = this.formatEditDate(this.schedule.start_date)
        this.editenddate = this.formatEditDate(this.schedule.end_date)
        this.editmax_member = this.schedule.max_member
        console.log(this.schedule)
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
    },
  },
  created() {
    this.getDetail();
    this.getAdvice();
    axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.SPOTS +`semi_list/`)
      .then(response => {
				this.spots2= response.data
				// console.log(this.spots)
      })
      .catch(error => {
        console.log(error.response);
      })
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
    margin-left:9%;
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
    margin-top: 3px;
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
    font-size:0.8vw;
    margin-left:10px;
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
.spotselect {
	border-bottom:1px #FF5E5E solid;
	width:80%;
	font-family: 'SCDream4';
  cursor: pointer;
}
.courseplusbtn {
	width:40%;
	color:#FF5E5E;
	border: 2px #FF5E5E solid; 
	border-radius:10px;
	font-size:1.4vw;
	outline: none;
  float:right;
  font-family: 'SCDream4';
}
.courseplusbtn:hover {
	/* background-color:#FF5E5E; */
	color:#FF5E5E;
}
.spottitle {
    font-family: 'SCDream4';
    font-size:1.3vw;
}
.spottime {
    font-family: 'SCDream4';
    font-size:0.8vw;
    margin-left:10px;
    color:#707070;
    display: block;
    margin-bottom: 5px;
}
.memtypeselect {
	display:inline-block;
	width:45%; 
	font-size:1.1vw; 
	font-family: 'SCDream5';
}

</style>