<template>
  <v-container style="padding:0;">
    <SpotMap :data="this.$attrs.data" :schedule="this.$attrs.schedule" class="cardmap"></SpotMap>

    <v-row style="display: flex; justify-content: space-around; margin-top: -5vw; margin-bottom: 1vw;">
      <img v-if="schedule.together==1" src="@/assets/friend.png" alt="" style="width: 8vw; z-index: 100;">
      <img v-if="!test" src="@/assets/trans.png" style="width: 4vw; z-index: 100;"/>
      <img v-if="schedule.advice==1" src="@/assets/help2.png" alt="" style="width: 8vw; z-index: 100;">
    </v-row>

    <button @click="GotoDetail(schedule.id)" class="SDtitle"><span>{{schedule.title}}</span></button>
  </v-container>
</template>

<script>
import SpotMap from '@/components/schedules/SpotMap.vue'
export default {
	name: 'ScheduleCard',
    components: {SpotMap},
    data() {
		return {
        item: '',
        schedule:[],
      }
    },
    computed: {
      test() {
        return (this.schedule.together * this.schedule.advice)
      }
    },
    created() {
      this.schedule =this.$attrs.schedule;
    },
    methods: {
      GotoDetail(schedule_id) {
        this.$router.push({name: 'DetailSchedule', params: {schedule_id: schedule_id}});
      }
    }
}
</script>

<style>
/* 마우스 포인트 안먹네 */
.cardmap:hover {
    cursor: pointer; 
}
.SDtitle {
  /* background-color:rgba( 255, 19, 19, 0.6 ); */
  background-color:#FF5E5E;
  width:100%;
  height:3vw;
  font-family: 'SCDream5';
  color:white;
  font-size:1.5vw;
  /* margin-top:-100px; */
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
}

</style>