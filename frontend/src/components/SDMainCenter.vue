<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col
        cols="12"
        sm="2"
      >
      </v-col>
      <v-col
        cols="12"
        sm="8"
      >
      <hr style=" background-color:#FF5E5E;">
      <div class="newSchedule">
        <div class="mb-3 mt-2">
          <h1 style="display:inline; color:#FF5E5E; font-size:2.7vw;">NEW</h1>
          <h3 style="display:inline; font-size:1.7vw;  "> 스케줄</h3>
          <button style="margin-left: 8px;width:2%; height:1vw; background-color:#FF5E5E;"></button>
          <span class="imo">동행 모집</span>
          <button style="margin-left: 8px; width:2%; height:1vw; background-color:#FF5E5E;"></button>
          <span class="imo">도움 요청</span>
          <button class="plusbtn">더보기</button> 
        </div>
        <div>
          <v-col
            cols="12"
            sm="4"
            style="display:inline-block; padding:6px;"
          >
          <ScheduleCard :data="'a'" :schedule="schedule" />
          </v-col>
          <v-col
            cols="12"
            sm="4"
            style="display:inline-block; padding:6px;"
          >
          <ScheduleCard :data="'b'" :schedule="schedule" />
          </v-col>
          <v-col
            cols="12"
            sm="4"
            style="display:inline-block; padding:6px;"
          >
          <ScheduleCard :data="'c'" :schedule="schedule"/>
          </v-col>
        </div>
      </div>
      <div class="BESTSD">
        <div class="newSchedule mb-3 mt-2">
          <h1 style="display:inline; color:#FF9617; font-size:2.7vw;">BEST</h1>
          <h3 style="display:inline; font-size:1.7vw;  "> 스케줄</h3> 
        </div>
      </div>
      <div class="HELPSD">
        <div class="newSchedule mb-3 mt-2">
          <h1 style="display:inline; color:#FF5E5E; font-size:2.7vw;">도움!</h1>
          <h3 style="display:inline; font-size:1.7vw;  "> 요청</h3> 
        </div>
      </div>
      </v-col>
      <v-col
        cols="12"
        sm="2"
      >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ScheduleCard from '@/components/ScheduleCard';
export default {
  components:{ScheduleCard},
  data() {
    return {
      schedule: 
        {
            "id": 38,
            "user": {
                "username": "Edgar3906",
                "nickname": "이동혁",
                "gender": "남성",
                "age": 28,
                "introduce": "",
                "profile_image": ""
            },
            "title": "서울 여행!",
            "overview": "주말동안 서울에 있는 관광 명소를 갈 생각이에요!!",
            "private": 1,
            "advice": 1,
            "together": 1,
            "scrap_count": 0,
            "start_date": "2020-11-06T18:00:00+09:00",
            "end_date": "2020-11-08T18:00:00+09:00",
            "max_member": 5,
            "member_type_pk": 4,
            "style_type_pk": 4,
            "user_pk": 24,
            "coords": [
                [37.5394, 127.065],
                [37.5348, 127.092],
                [37.6855, 127.073],
                [37.6855, 127.073],
                [37.5118, 127.059]
            ]
        },
    }
  }
}
</script>

<style>
.plusbtn {
    float:right;
    margin-top:2.5%;
    width:6%;
    font-size:1vw;
    height:2vw;
    border-radius:20px;
    background-color: #FF5E5E;
    color:white;
    outline:none;
    font-family: 'SCDream6'
}
</style>