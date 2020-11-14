<template>
  <v-row class="fill-height">
    <v-col>
      <!-- {{ this.$attrs.AllCourses}} -->
        <v-btn 
          class="datebtn" 
          @click="$refs.calendar.prev()"
          color="#FF5E5E"
        >
          Prev
        </v-btn>
        <!-- <v-btn style="margin-left:5%;" class="startendbtn" color="rgba( 13, 136, 255)" @click="$refs.calendar.move()">
          First
        </v-btn>
        <v-btn style="margin-left:1%;" class="startendbtn" color="rgba( 13, 136, 255)" @click="$refs.calendar.prev()">
          Last
        </v-btn> -->
        <v-btn 
          class="datebtn" 
          @click="$refs.calendar.next()"
          color="#FF5E5E"
          style="margin-left:25%;"
        >
          Next
        </v-btn>
      <v-sheet height="100%" width="97%">
        <v-calendar
            :start="formatDate(schedule.start_date)"
            :end ="formatDate(schedule.end_date)"
            ref="calendar"
            v-model="value"
            color="primary"
            type="4day"
            :events="events"
            :event-color="getEventColor"
            :event-ripple="false"
            @click:event="showEvent"
            @click:more="viewDay"
            @click:date="viewDay"
            @change="getInitialEvents"
            @mousedown:event="startDrag"
            @mousedown:time="startTime"
            @mousemove:time="mouseMove"
            @mouseup:time="endDrag"
            @mouseleave.native="cancelDrag"
            style="font-family: 'SCDream6'"
        >
          <template v-slot:event="{ event, timed, eventSummary }">
            <div
                class="v-event-draggable"
                v-html="eventSummary()"
            ></div>
            <div
                v-if="timed"
                class="v-event-drag-bottom"
                @mousedown.stop="extendBottom(event)"
            ></div>
          </template>
        </v-calendar>
        <!-- 모달창 -->
        <v-dialog
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          max-width="1000px"
          min-width="500px"
          offset-x
        >
          <v-card
            color="grey lighten-4"
            min-height="500px"
            flat
          >
            <!-- 모달 카드 헤더 -->
            <v-toolbar
              :color="Course.color"
              dark
            >
              <v-toolbar-title><h2>{{ Course.name }}</h2></v-toolbar-title>
              <v-spacer></v-spacer>
              <v-btn icon>
                <v-icon>mdi-heart</v-icon>
              </v-btn>
              <v-btn icon>
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </v-toolbar>

            <!-- 모달 카드 내용 -->
            <v-card-text style="padding-bottom:0px;">
              <v-row>
                <!-- <span>{{ Courses }}</span> -->
                <!-- 카드 왼쪽 -->
                <v-col
                  cols="9"
                  sm="6"
                >
                  <!-- 출발, 도착 시간 -->
                  <v-row class="time_outline">
                    <v-col cols="12" style="padding-bottom:0px;">
                      <h2 style="">일정 </h2> 
                      
                        <span style="font-family: 'SCDream6'; font-size:0.9rem; margin-left:60px;  ">{{formatDate2(Course.start_time)}}</span>
                        <span style="font-family: 'SCDream6'; font-size:0.9rem; margin-left:138px; ">{{formatDate2(Course.end_time)}}</span>
                      
                    </v-col>
                    <v-col
                      cols="6"
                      sm="6"
                      md="3"
                    >
                      <v-select
                        v-model="departureHour"
                        :items="Hours"
                        menu-props="auto"
                        label="출발(시)"
                        outlined
                        dense
                        hide-details
                      ></v-select>
                    </v-col>
                    <v-col
                      cols="6"
                      sm="6"
                      md="3"
                    >
                      <v-select
                        v-model="departureMinute"
                        :items="Minutes"
                        menu-props="auto"
                        label="출발(분)"
                        outlined
                        dense
                        hide-details
                      ></v-select>
                    </v-col>
                    <v-col
                      cols="6"
                      sm="6"
                      md="3"
                    >
                      <v-select
                        v-model="arrivalHour"
                        :items="Hours"
                        menu-props="auto"
                        label="도착(시)"
                        outlined
                        dense
                        hide-details
                      ></v-select>
                    </v-col>
                    <v-col
                      cols="6"
                      sm="6"
                      md="3"
                    >
                      <v-select
                        v-model="arrivalMinute"
                        :items="Minutes"
                        menu-props="auto"
                        label="도착(분)"
                        outlined
                        dense
                        hide-details
                      ></v-select>
                    </v-col>
                  </v-row>

                  <!-- 예산 -->
                  <v-row class="budget_outline" style="margin: 3px 0">
                    <v-row style="margin: 5px 5px 4px 12px;">
                      <div style="text-aling:center">
                        <h2>예산</h2>
                      </div>
                      <v-spacer></v-spacer>
                      <v-btn icon>
                        <v-icon>mdi-pencil</v-icon>
                      </v-btn>
                    </v-row>
                      <v-col
                        v-for="budget in budgets"  
                        :key="budget.budget_name"
                        cols="12"
                        style="padding: 0px 0px 4px 14px;"
                      >
                        <span style="font-family: 'SCDream6'; font-size:1.3rem;">{{budget.budget_name}}</span> 
                        <span style="font-family: 'SCDream5'; font-size:1.3rem;"> : {{budget.budget_value}}</span>
                        <v-spacer></v-spacer>
                      </v-col>
                  </v-row>
                  <!-- 메모 -->
                  <v-row class="budget_outline" style="margin: 3px 0">
                    <v-row style="margin: 5px 5px 4px 12px;">
                      <h2>메모</h2>
                    </v-row>
                    <v-row
                      class="memo_area"
                    >
                      <v-col
                        v-for="memo in Course.memos"
                        :key="memo"
                        cols="12"
                      >
                      </v-col>
                    </v-row>
                  </v-row>
                </v-col>


                <!-- 카드 오른쪽 -->
                <v-col
                  cols="3"
                  sm="6"
                  class="card-right-side"
                >
                  <v-row v-if="Course.spot_info" style="margin: 5px 5px 4px 12px;">
                    <h2>주소 : </h2>
                    <span style="font-family: 'SCDream6'; font-size:1.2rem; margin-bottom:3px;">{{ Course.spot_info.address}}</span>
                    <ScheduleDetailMap :lat="Course.spot_info.lat" :lon="Course.spot_info.lon" :item="Course.spot_info.id"/>
                    <img style="width:100%; height: 220px; margin-top:3px; border-radius:20px;" :src="Course.spot_info.image" alt="">
                  </v-row>
                  <v-row v-if="Course.custom_spot_info" style="margin: 5px 5px 4px 12px;">
                    <ScheduleDetailMap :lat="Course.custom_spot_info.lat" :lon="Course.custom_spot_info.lon" :item="Course.custom_spot_info.id"/>
                  </v-row>
                  <!-- <v-row -->
                    <!-- v-if="Object.keys(Courses.spot_info).includes('lat')"> -->
                    <!-- <SpotMap :lat="Courses.spot_info.lat" :lon="Courses.spot_info.lon"/> -->
                  <!-- </v-row> -->
                </v-col>
              </v-row>
            </v-card-text>

            <!-- 모달 하단 버튼 -->
            <v-card-actions>
              <v-btn
                class="text--white"
                color="#FF9617"
                @click="CourseUpdate"
              >
                수정
              </v-btn>
              <v-btn
                color="error"
                @click="CourseDelete"
              >
                삭제
              </v-btn>

              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                @click="selectedOpen = false"
              >
                닫기
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex'

import SERVER from '@/api/api'

import ScheduleDetailMap from '@/components/schedules/ScheduleDetailMap.vue'
import moment from 'moment';
import 'moment/locale/ko'
// 캘린더 시간은 ms 기준이다.
export default {
  name: "Calendar",
  components: {ScheduleDetailMap},
  data() {
    return {
      schedule:[],
      startcourseday: "2020-11-06",
      value: '',
      events: [],
      colors: ['#2196F3', '#FF5E5E' ,'#3F51B5', '#673AB7', '#00BCD4', '#4CAF50', '#FF9800', '#757575'],
      names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
      dragEvent: null,
      dragStart: null,
      createEvent: null,
      createStart: null,
      extendOriginal: null,
      Course:{},
      // Courses: [],
      budgets: [],
      budgets_names: ["식비", "교통비", "입장료", "숙소비", "기타"],
      selectedElement: null,
      selectedOpen: false,
      focus: '',

      // 출발, 도착 시간 변수
      Hours: [...Array(24)].map((v,i) => i+1),
      Minutes: [...Array(4)].map((v,i) => i*15),
      departureHour: null,
      departureMinute: null,
      arrivalHour: null,
      arrivalMinute: null,

      test: null
    }
  },
  props: {
    Courses: Array
  },
  created() {
    // 지금은 요청해서 받아오고 있음
    this.$http
      .get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SCHEDULE.SCHEDULES + this.$route.params.schedule_id, {
        // 'http://127.0.0.1:8000/schedule/38/', {
        headers: {
          Authorization: this.config,
        },
      })
      .then(res => {
        this.test = res.data
        // res.data.course.forEach(el => this.Courses.push(el))
        this.schedule = res.data.schedule
        console.log(this.schedule)
        this.getInitialEvents()
      })
    // console.log(this.$attrs.AllCourses)
    // DetailSchedule에서 내려받아서 각 코스를 Courses에 담기
    // DetailSchedule에서 내려받아서 하려고 했는데 created 시점에 비어있는 채로 SDdetail가 들어온뒤에 보이려고 해서
    // 캘린더가 안만들어지는 문제가 있음
    // this.$attrs.AllCourses.course.forEach(el => {
    //   this.Courses.push(el)
    // })
  },
  watch: {
		Courses: {
			deep: true,
			handler() {
        // console.log(1)
        this.getInitialEvents()
			}
		}
	},
  mounted () {
    this.$refs.calendar.checkChange()
  },
  computed: {
    ...mapGetters('accounts', ['config'])
  },
  methods: {
    formatDate(date) {
      moment.locale('ko');
      return moment(date).format('yyyy-MM-DD')
    },
    formatDate2(date) {
      moment.locale('ko');
      return moment(date).format('MM/DD dddd')
    },
    // allowedMinutes: v => v === 0 | v === 15 | v === 30 | v === 45,
    // 초기 이벤트 설정
    getInitialEvents () {
      const events = []
      const eventCount = this.Courses.length
      // 스케줄 코스 개수만큼 이벤트 생성하기
      for (let i = 0; i < eventCount; i++) {
        const timed = true
        const start = new Date(this.Courses[i].start_time).getTime()
        const end = new Date(this.Courses[i].end_time).getTime()
        // 서울로 시간을 맞추기 위해 9시간을 ms로 변환해서 더함
        // const datetimed = [new Date(start + (540 * 60 * 1000)), new Date(end + (540 * 60 * 1000))]
        this.Courses[i]["timed"] = timed
        if (this.Courses[i].spot_pk){
          this.Courses[i]["name"] = this.Courses[i].spot_info.title
        } else {
          this.Courses[i]["name"] = this.Courses[i].custom_spot_info.title
        }
        this.Courses[i]["start"] = this.roundTime(start)
        this.Courses[i]["end"] = this.roundTime(end)
        this.Courses[i]["color"] = this.rndElement(this.colors)
        // events.push({
        //   name: this.Courses[i].spot_info.title,
        //   color: this.rndElement(this.colors),
        //   start: this.roundTime(start),
        //   end: this.roundTime(end),
        //   timed,
        //   // datetimed
        // })
        events.push(this.Courses[i])
      }
      this.events = events
    },
    // 드래그 시작 이벤트 처리
    startDrag ({ event, timed }) {
      if (event && timed) {
        console.log('drag event start OK')
        this.dragEvent = event
        this.dragTime = null
        this.extendOriginal = null
      }
    },
    // 스케줄 확인 & 생성
    startTime (tms) {
      const mouse = this.toTime(tms)
      // 이미 있는 것을 드래그 or 클릭
      if (this.dragEvent && this.dragTime === null) {
        const start = this.dragEvent.start
        this.dragTime = mouse - start
      // 일정이 없는 비어있는 공간을 클릭
      } else {
        this.createStart = this.roundTime(mouse)
        this.createEvent = {
          name: `일정 #${this.events.length}`,
          color: this.rndElement(this.colors),
          start: this.createStart,
          end: this.createStart,
          timed: true,
        }
        this.events.push(this.createEvent)
      }
    },

    // 드래그를 아래로 할 경우 영역이 늘어남
    extendBottom (event) {
      this.createEvent = event
      this.createStart = event.start
      this.extendOriginal = event.end
    },
    // 마우스 움직이는 동안 처리
    mouseMove (tms) {
      const mouse = this.toTime(tms)
      // 이미 있는 이벤트 드래그
      if (this.dragEvent && this.dragTime !== null) {
        console.log(this.dragEvent)
        const start = this.dragEvent.start
        const end = this.dragEvent.end
        const duration = end - start
        const newStartTime = mouse - this.dragTime
        const newStart = this.roundTime(newStartTime)
        const newEnd = newStart + duration
        console.log(newStartTime, newStart, newEnd)

        this.dragEvent.start = newStart
        this.dragEvent.end = newEnd
      // 새로 생성되는 이벤트 드래그
      } else if (this.createEvent && this.createStart !== null) {
        const mouseRounded = this.roundTime(mouse, false)
        const min = Math.min(mouseRounded, this.createStart)
        const max = Math.max(mouseRounded, this.createStart)

        this.createEvent.start = min
        this.createEvent.end = max
      }
    },
    // 마우스를 떼면 드래그 끝내면서 초기화
    endDrag () {
      this.dragTime = null
      this.dragEvent = null
      this.createEvent = null
      this.createStart = null
      this.extendOriginal = null
    },
    // 마우스 드래그 취소
    cancelDrag () {
      if (this.createEvent) {
        if (this.extendOriginal) {
          this.createEvent.end = this.extendOriginal
        } else {
          const i = this.events.indexOf(this.createEvent)
          if (i !== -1) {
            this.events.splice(i, 1)
          }
        }
      }
      this.createEvent = null
      this.createStart = null
      this.dragTime = null
      this.dragEvent = null
    },
    // 시간 15분 단위로 맞추기위해 변환
    roundTime (time, down = true) {
      const roundTo = 15 // 15분 단위로 맞춰서 출력
      const roundDownTime = roundTo * 60 * 1000 // ms단위로 변환
      return down
          ? time - time % roundDownTime
          : time + (roundDownTime - (time % roundDownTime))
    },
    // dateTime ms로 변환한 시간 얻어오기
    toTime (tms) {
      return new Date(tms.year, tms.month - 1, tms.day, tms.hour, tms.minute).getTime()
    },
    getEventColor (event) {
      const rgb = parseInt(event.color.substring(1), 16)
      const r = (rgb >> 16) & 0xFF
      const g = (rgb >> 8) & 0xFF
      const b = (rgb >> 0) & 0xFF

      return event === this.dragEvent
          ? `rgba(${r}, ${g}, ${b}, 0.7)`
          : event === this.createEvent
              ? `rgba(${r}, ${g}, ${b}, 0.7)`
              : event.color
    },
    // 코스 하나 클릭 시 모달 보여주는 이벤트 관리
    showEvent ({ nativeEvent, event }) {
      // 이미 있는 코스 조회 시 데이터 엮어주기
      // console.log('showEvent !')
      this.departureHour = new Date(event.start).getHours()
      this.departureMinute = new Date(event.start).getMinutes()
      this.arrivalHour = new Date(event.end).getHours()
      this.arrivalMinute = new Date(event.end).getMinutes()
      this.budgets = []
      let idx = 0
      Object.keys(event).forEach(el => {
        if (el.includes('budget')) {
          this.budgets.push({
            original_name: el,
            budget_name: this.budgets_names[idx],
            budget_value: event[el]
          })
          idx += 1
        }
      })
      console.log(this.budgets)
      // 모달 열기
      const open = () => {
        this.Course = event
        // 모달창 열 위치를 정함
        this.selectedElement = nativeEvent.target
        setTimeout(() => {
          this.selectedOpen = true
        }, 10)
      }

      // 모달 닫기
      if (this.selectedOpen) {
        this.selectedOpen = false
        // 10ms 대기시간
        setTimeout(open, 10)
      } else {
        open()
      }
      nativeEvent.stopPropagation()
    },

    // Course U & D
    CourseDelete() {
      console.log(this.Courses.id)
    },
    CourseUpdate() {
      console.log('TRY Course Update')
    },
    // 숫자 랜덤(안씀)
    rnd (a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    // 이름, 컬러 랜덤(안씀)
    rndElement (arr) {
      return arr[this.rnd(0, arr.length - 1)]
    },
    // 날짜 랜덤(안씀)
    rndDate(start, end) {
      return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
    },
    // 일주일, 4일로 변경해서 볼 수 있게 하는 옵션 메서드(안씀)
    viewDay ({ date }) {
      this.focus = date
      this.type = 'day'
    },
  },
}
</script>

<style scoped>
.budget_outline {border: 2px solid black;border-radius: 20px}
.time_outline {border: 2px solid black;border-radius: 20px;margin: 5px 0; min-height:100px}
.memo_area {min-height: 160px}
.card-right-side {border: 2px solid black;border-radius: 20px; margin: 16px 0}
.v-event-draggable {
  font-size:1.2vw;
}
.datebtn {
  width:30%;
  font-size: 1.4vw;
  color:white;
  margin-bottom:5px;
}
.startendbtn {
  width:10%;
  font-size: 1.4vw;
  color:white;
  margin-bottom:5px;
}
</style>
