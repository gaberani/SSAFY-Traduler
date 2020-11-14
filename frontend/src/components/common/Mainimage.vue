<template>
<div class="mainimg">
	<div class="maincontent">
		<center>
			<h1 style="color:white; font-size:2.5vw;">국내 여행엔 Traduler!</h1>
			<p class="mainp">OOOOO개의 여행지 데이터를 활용한 </p>
			<p class="mainp">추천과 스케쥴러를 사용해</p>
			<p class="mainp">여행을 계획해보세요!</p>
			<!-- <button class="mainbtn">Traduler 시작</button> -->
			<v-dialog
					v-model="dialog"
					max-width="500"
			>
				<template v-slot:activator="{ on, attrs }">
				<button
					class="mainbtn"
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
					<v-text-field
						dense
						label="스케줄 제목"
						style="width:80%; font-size:1.5vw; font-family: 'SCDream6'; border:'#FF5E5E'"
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
						style="width:25%; font-size:1vw; font-family: 'SCDream5'; "
						v-model="max_member"
						hide-details
					></v-text-field>
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
									hide-details
									style="width:50%; font-family: 'SCDream5'; "
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
								<input type="checkbox" v-model="together">
							</div>
							<div v-else>
								<img src="@/assets/friend.png" style="width:5%; height:1.1vw;" ><span style="margin-right:2px;font-family: 'SCDream4';font-size:1.1vw;">동행 모집</span>
								<input disabled type="checkbox" v-model="together">
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
				together:false,
				advice:false,
				member_type:'',
				travel_type:'',
				startdate: '',
				enddate: '',
				max_member:1,
				menu3: false,
				menu2: false,
				member : ['혼자','가족','커플','3인이상'],
				type : ['힐링','액티비티','맛집 탐방','역사 탐방'],
				formatstartdate:'',
				formatenddate:'',
      }
		},
		computed: {
    ...mapGetters('accounts', ["config",]),
		},
    methods: {
			createScheduler() {
				if (this.title.length !=0 && this.overview.length !=0 && this.startdate.length !=0 &&
				this.enddate.length !=0 ) {
				this.formatstartdate = this.startdate + 'T00:00:00+09:00'
				this.formatenddate = this.enddate + 'T23:59:00+09:00'
				let createbody = {"schedule_info":{
					title : this.title,
					overview :this.overview,
					private : this.privatebtn,
					advice : this.advice*1,
					together : this.together*1,
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
			}
    },
}
</script>

<style>
.mainimg {
    background-image : url("../../assets/mainimage.jpg");
    background-size:cover;
    width:100%;
    min-height: 35vw;
    background-position: center;
    filter:saturate(150%);
}
.maincontent {
    float:right;
    margin-top:7%;
    margin-right:15%;
}
.mainp {
    color:white;
    font-size:1.2vw;
    font-family: 'SCDream4'
}
.mainbtn {
    font-family: 'SCDream8';
    color:white;
    font-size:1.4vw;
    width:55%;
    height:3vw;
    background-color: rgba( 255, 19, 19, 0.55 );
    border-radius:25px;
}
.memtypeselect {
	display:inline-block;
	width:45%; 
	font-size:1.1vw; 
	font-family: 'SCDream5';
}
</style>