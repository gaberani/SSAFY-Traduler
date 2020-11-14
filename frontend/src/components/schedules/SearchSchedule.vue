<template>
    <div>
        <div class="schedulemainimg">
            <center>
              <v-dialog
                v-model="dialog"
                max-width="500"
              >
              <template v-slot:activator="{ on, attrs }">
              <button
                class="schedulemainbtn"
                v-bind="attrs"
                v-on="on"
              >
                Traduler 시작
              </button>
              </template>
              <v-card>
              <v-card-title class="headline" >
                <span style="font-family: 'SCDream5';font-size:1.5rem; margin-bottom:5px;">
              
                스케줄 생성
                </span>
              </v-card-title>
              <center>
                <v-row no-gutters style="display:block;">
                <v-text-field
                  dense
                  label="스케줄 제목"
                  style="width:80%; font-size:1.5vw; font-family: 'SCDream6'; "
                  v-model="title"
                ></v-text-field>
                <v-text-field
                  dense
                  label="스케줄 Overview"
                  style="width:90%; font-size:1.2vw; font-family: 'SCDream5'; "
                  v-model="overview"
                ></v-text-field>
                <v-select
                  :items="member"
                  label="멤버 타입"
                  class="memtypeselect"
                  v-model="member_type"
                ></v-select>
                <v-select
                  :items="type"
                  label="컨셉"
                  class="memtypeselect"
                  style="margin-left:5px;"
                  v-model="travel_type"
                ></v-select>
                <v-text-field
                  dense
                  type="number"
                  label="참여 인원(명)"
                  placeholder="숫자로 입력해주세요."
                  style="width:25%; font-size:1vw; font-family: 'SCDream5';"
                  v-model="max_member"
                  hide-details
                ></v-text-field>
                <br>
                <v-menu
                    v-model="menu4"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    transition="scale-transition"
                    offset-y
                    width="50%"
                    >
                    <template v-slot:activator="{ on, attrs }" >
                        <v-text-field
                        v-model="startdate2"
                        placeholder="가는날 (이후)"
                        prepend-icon="mdi-car"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                        hide-details
                        style="width:50%; font-family: 'SCDream5'; margin-top:-20px;"
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        v-model="startdate2"
                        @input="menu4 = false"
                    ></v-date-picker>
                </v-menu>
                <v-menu
                  v-model="menu5"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  >
                  <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                      v-model="enddate2"
                      placeholder="오는날 (이전)"
                      prepend-icon="mdi-home"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      style="width:50%; font-family: 'SCDream5';"
                      ></v-text-field>
                  </template>
                  <v-date-picker
                      v-model="enddate2"
                      @input="menu5 = false"
                  ></v-date-picker>
              </v-menu>
                </v-row>
                <v-row no-gutters >
                  <v-col
                    cols="12"
                    sm="6"
                  >
                    <div style="font-family: 'SCDream5'; font-size:1.3vw;">
                      <span style="margin-right:2px;">공개</span><input class="privateradio" type="radio" name="private" v-model="privatebtn" value="0">
                    </div>
                    <div v-if="privatebtn=='0'">
                      <img src="@/assets/friend.png" style="width:5%; height:1.1vw;" ><span style="margin-right:2px;font-family: 'SCDream4';font-size:1.1vw;">동행 모집</span>
                      <input type="checkbox" v-model="together2">
                    </div>
                    <div v-else>
                      <img src="@/assets/friend.png" style="width:5%; height:1.1vw;" ><span style="margin-right:2px;font-family: 'SCDream4';font-size:1.1vw;">동행 모집</span>
                      <input disabled type="checkbox" v-model="together2">
                    </div>
                    <div v-if="privatebtn=='0'">
                      <img src="@/assets/help2.png" style="width:5%; height:1.1vw;"><span style="margin-right:2px;font-family: 'SCDream4';font-size:1.1vw;">도움 요청</span>
                      <input type="checkbox" v-model="advice">
                    </div>
                    <div v-else>
                      <img src="@/assets/help2.png" style="width:5%; height:1.1vw;"><span style="margin-right:2px;font-family: 'SCDream4';font-size:1.1vw;">도움 요청</span>
                      <input disabled type="checkbox" v-model="advice">
                    </div>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    style="border-left:2px #707070 solid;"
                  >
                    <div style="font-family: 'SCDream5'; font-size:1.3vw;">
                      <span style="margin-right:2px;">비공개</span><input class="privateradio" type="radio" name="private" v-model="privatebtn" value="1">
                    </div>
                  </v-col>
                </v-row>
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
                  @click="createScheduler"
                  >
                  생성
                  </v-btn>
              </v-card-actions>
              </v-card>
            </v-dialog>
          </center>
        </div>
        <div>
            <center>
            <div class="SDsearchbox">
                <!-- 셀렉트박스 -->
                <!-- <select class="SDsearchselect" v-model="SDselect">
                    <option value="title" >제목</option>
                    <option value="writer" >작성자</option>
                </select> -->
                <!-- v-model="query" -->
                <!-- 검색바 -->
                <!-- v-if="SDselect=='title'" -->
                <input class="schedulesearch" placeholder="원하는 제목을 입력하세요." v-model="query">
                <!-- <input v-else class="schedulesearch" placeholder="원하는 작성자를 입력하세요."> -->
                <button @click.prevent="searchschedule" class="searchbtn" ><i style="font-size:1.4vw" class="fas fa-search"></i></button>
            </div>
            <div class="SDfilterbox">
                <!-- 필터 -->
                <!-- 1. 지역 필터 -->
                <v-row style="width:80%;">
                    <v-col
                    cols="1.5">

                    </v-col>
                    <v-col
                    cols="1.5"
                    style="border-right:2px #707070 solid;">
                    <select class="selectspot" style="margin-top:12px;" v-model="area_code">
                        <option value="">지역</option>
                        <option value="A">서울</option>
                        <option value="B">인천</option>
                        <option value="C">대전</option>
                        <option value="D">대구</option>
                        <option value="E">광주</option>
                        <option value="F">부산</option>
                        <option value="G">울산</option>
                        <option value="H">세종</option>
                        <option value="I">경기도</option>
                        <option value="J">강원도</option>
                        <option value="K">충청북도</option>
                        <option value="L">충청남도</option>
                        <option value="M">경상북도</option>
                        <option value="N">경상남도</option>
                        <option value="O">전라북도</option>
                        <option value="P">전라남도</option>
                        <option value="Q">제주도</option>
                    </select>
                    </v-col>
                    <v-col
                    cols="2"
                    style="border-right:2px #707070 solid;" >
                        <input type="radio" name="size" id="size_1" />
                        <label class="radiobox" for="size_1" style="width:45%;" @click="changememIdx(1)" :class="{noCheck: checkList[memberIdx][0]}">혼자</label>

                        <input type="radio" name="size" id="size_2" />
                        <label class="radiobox" for="size_2" style="width:45%;" @click="changememIdx(2)" :class="{noCheck: checkList[memberIdx][1]}">가족</label>

                        <input type="radio" name="size" id="size_3" />
                        <label class="radiobox" for="size_3" style="width:45%;" @click="changememIdx(3)" :class="{noCheck:checkList[memberIdx][2]}">커플</label>

                        <input type="radio" name="size" id="size_4" />
                        <label class="radiobox" for="size_4" style="width:45%;" @click="changememIdx(4)" :class="{noCheck: checkList[memberIdx][3]}">3인이상</label>
                    </v-col>
                    <v-col
                    cols="2"
                    style="border-right:2px #707070 solid;">
                        <input type="radio" name="typeS" id="typeS_1" />
                        <label class="radiobox" for="typeS_1" style="width:45%;" @click="changetypeIdx(1)" :class="{noCheck: checkList[typeIdx][0]}">힐링</label>

                        <input type="radio" name="typeS" id="typeS_2" />
                        <label class="radiobox" for="typeS_2" style="width:45%;" @click="changetypeIdx(2)" :class="{noCheck: checkList[typeIdx][1]}">액티비티</label>

                        <input type="radio" name="typeS" id="typeS_3" />
                        <label class="radiobox" for="typeS_3" style="width:45%;" @click="changetypeIdx(3)" :class="{noCheck: checkList[typeIdx][2]}">맛집 탐방</label>

                        <input type="radio" name="typeS" id="typeS_4"/>
                        <label class="radiobox" for="typeS_4" style="width:45%;" @click="changetypeIdx(4)" :class="{noCheck: checkList[typeIdx][3]}">역사 탐방</label>
                    </v-col>
                    <v-col
                    cols="1.2"
                    style="border-right:2px #707070 solid; margin-right:5px;">
                        <input v-model="together" type="checkbox" class="checkinput" name="together" id="together" style="margin-top:10px;"/>
                        <label class="check" for="together"> 동행 모집중 😊</label>
                        <br>
                        <input v-model="help" type="checkbox" class="checkinput" name="help" id="help"/>
                        <label class="check" for="help"> 도움 요청중 😊</label>
                    </v-col>
                    <v-col
                    cols="2"
                    >
                    <v-menu
                        v-model="menu2"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="100px"
                        >
                        <template v-slot:activator="{ on, attrs }" >
                            <v-text-field
                            v-model="startdate"
                            placeholder="가는날 (이후)"
                            prepend-icon="mdi-car"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            hide-details
                            class="startendtext"
                            ></v-text-field>
                        </template>
                        <v-date-picker
                            v-model="startdate"
                            @input="menu2 = false"
                        ></v-date-picker>
                    </v-menu>
                    <v-menu
                        v-model="menu3"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="100px"
                        >
                        <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                            v-model="enddate"
                            placeholder="오는날 (이전)"
                            prepend-icon="mdi-home"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            hide-details
                            class="startendtext"
                            ></v-text-field>
                        </template>
                        <v-date-picker
                            v-model="enddate"
                            @input="menu3 = false"
                        ></v-date-picker>
                    </v-menu>
                    </v-col>
                    <v-col
                    cols="1.8">

                    </v-col>
                </v-row>
            
            </div>
            </center>
        </div>
    </div>
</template>

<script>
import SERVER from '@/api/api'
import axios from 'axios'
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      title:'',
      overview:'',
      dialog:false,
      privatebtn:"1",
      together2:false,
      advice:false,
      member_type:'',
      travel_type:'',
      startdate2: '',
      enddate2: '',
      max_member:1,
      menu5: false,
      menu4: false,
      member : ['혼자','가족','커플','3인이상'],
      type : ['힐링','액티비티','맛집 탐방','역사 탐방'],
      formatstartdate:'',
      formatenddate:'',
      SDselect: 'title',
      area_code: '',
      memberIdx: 0,
      typeIdx: 0,
      startdate: '',
      enddate: '',
      menu3: false,
      menu2: false,
      together: true,
      help: true,
    //   보낼 때 together * 1
      checkList : [[true,true,true,true], [false, true, true, true], [true, false, true, true], [true, true, false, true], [true, true, true, false]],
    // category_code: '',
    // area_code: '',
      query: '',
    }
  },
  computed: {
    searchMemberIdx() {
      return (this.memberIdx===0 ? '' : this.memberIdx)
    },
    searchStyleIdx() {
      return (this.typeIdx===0 ? '' : this.typeIdx)
    },
    ...mapGetters('accounts', ["config",]),
  },
  methods: {
    createScheduler() {
			if (this.title.length !=0 && this.overview.length !=0 && this.startdate2.length !=0 &&
				this.enddate2.length !=0 ) {
				this.formatstartdate = this.startdate2 + 'T00:00:00+09:00'
				this.formatenddate = this.enddate2 + 'T23:59:00+09:00'
				let createbody = {"schedule_info":{
					title : this.title,
					overview :this.overview,
					private : this.privatebtn,
					advice : this.advice*1,
					together : this.together2*1,
					member_type_pk: this.changeMemtype(),
					style_type_pk: this.changeStyletype(),
					start_date: this.formatstartdate,
					end_date: this.formatenddate,
					max_member: this.max_member,
        }}
        axios.post(process.env.VUE_APP_SERVER_URL +  SERVER.URL.SCHEDULE.SCHEDULES, createbody, {
            headers: {
							Authorization : this.config,
				}})
				.then(response => {
					console.log(response)
					alert("스케줄이 생성되었습니다.")
					this.$router.push({name: 'DetailSchedule', params: {schedule_id: response.data.schedule_pk}})
				})
				.catch(error => { 
					console.log(error.response)
				})} else {
					alert("빈칸을 채워주세요!!")
				}
			},
			changeMemtype() {
				return this.member.indexOf(this.member_type) +1
			},
			changeStyletype() {
				return this.type.indexOf(this.travel_type) +1
			},
    searchschedule() {
      this.$router.push({name: 'Scheduleresult', query: {
        title: this.query,
        area: this.area_code,
        member_type: this.searchMemberIdx,
        style_type: this.searchStyleIdx,
        together: this.together * 1,
        advice: this.help * 1,
        start_data: this.startdate,
        end_date: this.end_date
      }})
    },
    changememIdx(number) {
      if (this.memberIdx === number) {
        this.memberIdx = 0;
      } else {
        this.memberIdx = number;
      }
    },
    changetypeIdx(number) {
      if (this.typeIdx === number) {
        this.typeIdx = 0;
      } else {
        this.typeIdx = number;
      }
    }
  },
}
</script>

<style scoped>
.schedulemainimg {
    background-image : url("../../assets/schedulemain.jpg");
    background-size:cover;
    width:100%;
    min-height: 35vw;
    /* background-position: center; */
}
.schedulemainbtn {
    font-family: 'SCDream8';
    color:white;
    font-size:1.4vw;
    width:18%;
    min-width: 200px;
    height:3vw;
    background-color: rgba( 13, 136, 255, 0.65 );
    border-radius:25px;
    margin-top:17vw;
    min-height: 30px;
}
.SDsearchbox {
    margin-top:10px;
}
.schedulesearch {
    width:40%;
    height:37px;
    background-color:white;
    border:3px #FF1313 solid;
    border-radius:50px;
    outline:none;
    padding-left: 10px;
    margin-top:10px;
    font-size:1vw;
    font-family: 'SCDream5'
}
.SDsearchselect {
    width:5%;
    min-width: 50px;
    height:37px;
    background-color:white;
    border:3px #FF1313 solid;
    border-radius:50px;
    padding-left: 5px;
    outline:none;
    margin-top:10px;
    margin-right:5px;
    font-size:1vw;
    font-family: 'SCDream5';
    appearance: button;
}
.selectspot {
    height:30px;
    min-width:46px;
    width:55%;
    background-color:white;
    border:2px #EB7878 solid;
    outline:none;
    appearance: button;
    font-size:0.9vw;
    color: #EB7878;
    font-family: 'SCDream5';
    margin-top:7%;
    float:right;
    margin-right:5%;
}
.SDfilterbox {
    margin-top:15px;
}
.col {
    padding:0;
}
input[type="radio"]{
  visibility: hidden;
  height: 0;
  width: 0;
}

.radiobox {
  display: inline-block;
  margin:3px;
  vertical-align: middle;
  text-align: center;
  cursor: pointer;
  /* background-color: #454545; */
  font-family: 'SCDream5';
  border: 2px #454545 solid ; 
  color: #454545;
  padding: 3px 8px;
  border-radius: 3px;
  font-size:0.7vw;
  min-width: 40px;
}
input[type="radio"]:checked + label{
  border: 2px #EB7878 solid;
  color:#EB7878;
}
.searchbtn {
    background-color:#EB7878;
    width:5%;
    height:37px;
    outline:none;
    min-width:50px;
    border-radius:50px;
    color:white;
    margin-left:3px;
}
.noCheck {
    border: 2px #454545 solid !important ; 
    color: #454545  !important;
}
.check {
    font-family: 'SCDream4';
    font-size:0.9vw;
    color: #454545
}
.startendtext {
    padding:0;
    margin: 0;
    font-size: 0.9vw;
    width:70%;
    font-family: 'SCDream4';
    float: left;
}
.memtypeselect {
	display:inline-block;
	width:45%; 
	font-size:1.1vw; 
	font-family: 'SCDream5';
}
.privateradio {
  visibility: visible !important;
  width:12.8px !important;
  height:12.8px !important;
}
</style>