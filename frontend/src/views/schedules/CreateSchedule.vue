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
				<v-text-field
					dense
					label="스케줄 제목"
					style="width:80%; font-size:2.2vw; font-family:'jalnanregular'; border:'#FF5E5E'"
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
          label="인원"
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
							<div v-for="(cour,idx) in createcourse" :key="cour.id">
								<p v-if="idx!=0" style="font-size:1.6rem; margin-left:-15px; margin-bottom:5px;"><i class="fas fa-car"></i></p>
								<button class="courseidx" style="background-color:">{{idx+1}}</button>
								<span class="spottitle">{{cour.spot_info.title}}</span>
								<span class="spottime">{{formattime(cour.start_time)}} ~ {{formattime(cour.end_time)}}</span>
							</div>
						</div>
						<v-dialog
							v-model="dialog"
							max-width="300"
						>
							<template v-slot:activator="{ on, attrs }">
								<v-btn
									class="courseplusbtn"
									v-bind="attrs"
									v-on="on"
								>
									+
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
										v-model="spot" 
										:options="spots" 
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
										@click="dialog = false"
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
						<i class="fas fa-check-circle car" style="font-size:2rem; color:blue;"></i>
					</v-col>
				</div>
			</v-col>
			<v-col
					cols="12"
					sm="7"
					style="margin-top:25px;"
        >  
				<Calendar/>
      </v-col>
			<v-col
					cols="12"
					sm="2"
        >
				<v-row style="position:fixed; bottom:6%; right:2%; width:15%;">
					<v-col
						cols="12"
						sm="12"
					>
						<div style="border:2px #FF5E5E solid; width:100%; font-family: 'SCDream5'; font-size:1.3vw; border-radius:10px;">
							<div style="margin-left:5px;">	
								<div>
									<span>공개</span><input type="radio" name="private" v-model="privatebtn" value="yes">
								</div>
								<div v-if="privatebtn=='yes'">
									<img src="@/assets/friend.png" style="width:13%; height:1.1vw;" ><span style="font-family: 'SCDream4';font-size:1.1vw;">동행 모집</span>
									<input type="checkbox" v-model="together">
								</div>
								<div v-else>
									<img src="@/assets/friend.png" style="width:13%; height:1.1vw;" ><span style="font-family: 'SCDream4';font-size:1.1vw;">동행 모집</span>
									<input disabled type="checkbox" v-model="together">
								</div>
								<div v-if="privatebtn=='yes'">
									<img src="@/assets/help2.png" style="width:13%; height:1.1vw;"><span style="font-family: 'SCDream4';font-size:1.1vw;">도움 요청</span>
									<input type="checkbox" v-model="advice">
								</div>
								<div v-else>
									<img src="@/assets/help2.png" style="width:13%; height:1.1vw;"><span style="font-family: 'SCDream4';font-size:1.1vw;">도움 요청</span>
									<input disabled type="checkbox" v-model="advice">
								</div>
								<div>
									<span>비공개</span><input type="radio" name="private" v-model="privatebtn" value="no">
								</div>
							</div>
						</div>
					</v-col>
					<v-col
						cols="12"
						sm="12"
					>
						<center>
							<button class="savebtn">저장</button>
						</center>
					</v-col>
				</v-row>
			</v-col>
		</v-row>
	</v-app>
</template>

<script>
import Calendar from '@/components/schedules/Calendar.vue'
import SERVER from '@/api/api'
import axios from 'axios'
import Multiselect from 'vue-multiselect'

import moment from 'moment';
import 'moment/locale/ko'
export default {
	components: {
		Calendar,
		Multiselect
	},
	data() {
		return {
			privatebtn:"no",
			together:false,
			advice:false,
			spot:'',
			spots:[],
			title:'',
			overview:'',
			member_type:'',
			travel_type:'',
			startdate: '',
      enddate: '',
      menu3: false,
      menu2: false,
			member : ['혼자','가족','커플','3인이상'],
			type : ['힐링','액티비티','맛집 탐방','역사 탐방'],
			createcourse: [],
			dialog:false,
			selectarea:['전체','서울','인천','대구','광주','부산','울산','세종','경기도','강원도',
			'충청북도','충청남도','경상북도','경상남도','전라북도','전라남도','제주도'],
			// 출발, 도착 시간 변수
      DHours: [...Array(24)].map((v,i) => i+1),
      DMinutes: [...Array(4)].map((v,i) => i*15),
      DdepartureHour: null,
      DdepartureMinute: '00',
      DarrivalHour: null,
			DarrivalMinute: '00',
			coursestarttime:'',
			courseendtime:''
		}
	},
	methods: {
		formatDate(date) {
      moment.locale('ko');
      return moment(date).format('dddd, MM월 DD일')
    },
    formattime(time) {
      moment.locale('ko');
      return moment(time).format('MM월 DD일 a hh:mm')
		},
		spotWithTitle({title}) {
			return `${title}`
		},
		schedulePlus() {
			console.log(this.DdepartureHour.length)
			if (this.spot && this.startdate && this.DdepartureHour &&
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
				console.log(this.DdepartureHour)
				this.schedulePlusunit()
			} 
		},
		schedulePlusunit() {
			this.coursestarttime = this.startdate + 'T' +this.DdepartureHour +':'+this.DdepartureMinute+':00+09:00'
			this.courseendtime = this.enddate + 'T' +this.DarrivalHour +':'+this.DarrivalMinute+':00+09:00'
			this.createcourse.push({
				'spot_info' : { 
					'title':this.spot.title
				},
				'start_time' : this.coursestarttime,
				'end_time' : this.courseendtime,
			})
			console.log(this.createcourse)
			console.log(this.spot.title)
			console.log(this.coursestarttime)
			console.log(this.courseendtime)
			this.dialog = false
		}
	},
	created() {
		axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.SPOTS +`semi_list/`)
      .then(response => {
				this.spots= response.data
				// console.log(this.spots)
      })
      .catch(error => {
        console.log(error.response);
      })
	},
}
</script>

<style>
.memtypeselect {
	display:inline-block;
	width:45%; 
	font-size:1.1vw; 
	font-family: 'SCDream5';
}
.courseplusbtn {
	width:110%;
	color:#FF5E5E;
	border: 2px #FF5E5E solid; 
	border-radius:10px;
	font-size:1.4vw;
	outline: none;
}
.courseplusbtn:hover {
	/* background-color:#FF5E5E; */
	color:#FF5E5E;
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
.savebtn {
	border:3px #FF5E5E solid; 
	width:100%; 
	display:block; 
	border-radius:20px; 
	font-size:1.5vw; 
	font-family: 'SCDream4';
}
.savebtn:hover {
	background-color:#FF5E5E;
	color:white;
}
.spotselect {
	border-bottom:1px #FF5E5E solid;
	width:80%;
	font-family: 'SCDream4';
}
</style>