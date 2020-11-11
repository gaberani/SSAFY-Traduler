<template>
  <v-container style="padding:0;">
      <!-- v-if -->
      <img v-if="schedule.together==1" class="togetherimo" src="../assets/friend.png" alt="">
      <!-- v-if -->
      <!-- <img class="helpimo" src="../assets/help.png" alt=""> -->
      <img v-if="schedule.advice==1" class="helpimo" src="../assets/help2.png" alt="">
    <SpotMap :data="this.$attrs.data" :schedule="this.$attrs.schedule" class="cardmap"></SpotMap>
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
    created() {
        this.schedule =this.$attrs.schedule
        // console.log(this.schedule)
    },
    methods: {
        GotoDetail(SDid) {
            this.$router.push('/detailschedule?id='+ SDid)
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
.togetherimo {
    z-index:2; 
    /* background-color:#FF9617;  */
    position:absolute; float:left; 
    margin-top:14.5%;
    height:3vw; 
    width:3%;
    outline: none;
    margin-left:1.7%;
}
.helpimo {
    z-index:2; 
    position:absolute; float:left; 
    margin-top:14.5%;
    height:3vw; 
    width:3%;
    outline: none;
    margin-left:16.4%;
}
</style>