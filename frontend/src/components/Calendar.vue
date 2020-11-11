<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="600">
        <v-calendar
            start="2020-11-06"
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
        <v-menu
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          offset-x
        >
          <v-card
            color="grey lighten-4"
            min-width="350px"
            flat
          >
            <v-toolbar
              :color="Courses.color"
              dark
            >
              <v-toolbar-title v-html="Courses.name"></v-toolbar-title>
              <v-spacer></v-spacer>
              <v-btn icon>
                <v-icon>mdi-heart</v-icon>
              </v-btn>
              <v-btn icon>
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </v-toolbar>

            <v-card-text>
              <v-row>
                <span>{{ Courses }}</span>
                <v-col
                    cols="12"
                    sm="6"
                    md="6"
                >
<!--                  <v-time-picker-->
<!--                      v-model="departureTime"-->
<!--                      full-width-->
<!--                      :allowed-minutes="allowedMinutes"-->
<!--                  >-->
<!--                    <v-spacer></v-spacer>-->
<!--                  </v-time-picker>-->
                </v-col>
                <v-col
                  cols="12"
                  sm="6"
                  md="6"
                >
<!--                  <v-time-picker-->
<!--                      v-model="arrivalTime"-->
<!--                      full-width-->
<!--                      :allowed-minutes="allowedMinutes"-->
<!--                  >-->
<!--                    <v-spacer></v-spacer>-->
<!--                  </v-time-picker>-->
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-btn
                text
                color="secondary"
                @click="selectedOpen = false"
              >
                Cancel
              </v-btn>
              <v-btn
                text
                color="warning"
                @click="TimeTest"
              >
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex'

// 캘린더 시간은 ms 기준이다.
export default {
  name: "Calendar",
  data() {
    return {
      startcourseday: '2020-11-08',
      value: '',
      events: [],
      colors: ['#2196F3', '#3F51B5', '#673AB7', '#00BCD4', '#4CAF50', '#FF9800', '#757575'],
      names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
      dragEvent: null,
      dragStart: null,
      createEvent: null,
      createStart: null,
      extendOriginal: null,

      Courses: [],
      selectedElement: null,
      selectedOpen: false,
      focus: '',
      departureTime: null,
      arrivalTime: null,
    }
  },
  created() {
    this.$http
      .get('http://127.0.0.1:8000/schedule/38/', {
        headers: {
          Authorization: this.config,
        },
      })
      .then(res => {
        res.data.course.forEach(el => this.Courses.push(el))
        this.getInitialEvents()
      })
  },
  mounted () {
    this.$refs.calendar.checkChange()
  },
  computed: {
    ...mapGetters(['config'])
  },
  methods: {
    // allowedMinutes: v => v === 0 | v === 15 | v === 30 | v === 45,
    // 초기 이벤트 설정
    getInitialEvents () {
      const events = []
      const eventCount = this.Courses.length
      // 스케쥴 코스 개수만큼 이벤트 생성하기
      for (let i = 0; i < eventCount; i++) {
        const timed = true
        const start = new Date(this.Courses[i].start_time).getTime()
        const end = new Date(this.Courses[i].end_time).getTime()
        // 서울로 시간을 맞추기 위해 9시간을 ms로 변환해서 더함
        const datetimed = [new Date(start + (540 * 60 * 1000)), new Date(end + (540 * 60 * 1000))]
        events.push({
          name: this.Courses[i].spot_info.title,
          color: this.rndElement(this.colors),
          start: this.roundTime(start),
          end: this.roundTime(end),
          timed,
          datetimed
        })
      }
      this.events = events
    },
    // 드래그 시작 이벤트 처리
    startDrag ({ event, timed }) {
      if (event && timed) {
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
        // console.log(new Date(mouse) + '//' + new Date(start) +'//'+ new Date(this.dragEvent.end))
      // 일정이 없는 비어있는 공간을 클릭
      } else {  //
        // 모달 CalendarCreate로 수정해도 괜찮을듯
        this.createStart = this.roundTime(mouse)
        this.createEvent = {
          name: `일정 #${this.events.length}`,
          color: this.rndElement(this.colors),
          start: this.createStart,
          end: this.createStart,
          timed: true,
          datetimed: tms
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

      if (this.dragEvent && this.dragTime !== null) {
        const start = this.dragEvent.start
        const end = this.dragEvent.end
        const duration = end - start
        const newStartTime = mouse - this.dragTime
        const newStart = this.roundTime(newStartTime)
        const newEnd = newStart + duration
        this.dragEvent.start = newStart
        this.dragEvent.end = newEnd
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

    // 숫자 랜덤
    rnd (a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    // 이름, 컬러 랜덤
    rndElement (arr) {
      return arr[this.rnd(0, arr.length - 1)]
    },
    // 날짜 랜덤
    rndDate(start, end) {
      return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
    },

    viewDay ({ date }) {
      this.focus = date
      this.type = 'day'
    },
    // 스케줄 하나 클릭 시 모달 관리
    showEvent ({ nativeEvent, event }) {
      const open = () => {
        this.Courses = event
        this.selectedElement = nativeEvent.target
        setTimeout(() => {
          this.selectedOpen = true
        }, 10)
      }

      if (this.selectedOpen) {
        this.selectedOpen = false
        setTimeout(open, 10)
      } else {
        open()
      }
      nativeEvent.stopPropagation()
    },
    TimeTest() {
      console.log(this.departureTime, this.arrivalTime)
    }
  },
}
</script>

<style scoped>

</style>