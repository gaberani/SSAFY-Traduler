<template>
  <v-container style="padding:0;">
      <!-- v-if -->
      <img class="togetherimo" src="../assets/friend.png" alt="">
      <!-- v-if -->
      <!-- <img class="helpimo" src="../assets/help.png" alt=""> -->
      <img class="helpimo" src="../assets/help2.png" alt="">
    <SpotMap :data="this.$attrs.data" :schedule="this.$attrs.schedule" class="cardmap"></SpotMap>
    <button class="SDtitle"><span>{{schedule.title}}</span></button>
  </v-container>
</template>

<script>
import SpotMap from '@/components/SpotMap.vue'
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
        console.log(this.schedule)
    }
}
</script>

<style>
.cardmap {
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
}
.togetherimo {
    z-index:10; 
    /* background-color:#FF9617;  */
    position:absolute; float:left; 
    margin-top:14.5%;
    height:3vw; 
    width:3%;
    outline: none;
    margin-left:1.7%;
}
.helpimo {
    z-index:30; 
    position:absolute; float:left; 
    margin-top:14.5%;
    height:3vw; 
    width:3%;
    outline: none;
    margin-left:16.4%;
}
</style>