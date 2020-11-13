<template>
  <div>
    <v-row style="text-align: center;">
      <v-col cols="5">
        <h3>스케줄</h3>
      </v-col>
      <v-col cols="5">
        <h3>상세 정보</h3>
      </v-col>
      <v-col cols="2">
        <h3>비고</h3>
      </v-col>
    </v-row>
    <v-row v-for="receive in receiveds" :key="receive.id" style="border-bottom: 1px solid black;">
      <v-col cols="5">
        <ScheduleCard :data="receive.id" :schedule="receive.schedule" />
      </v-col>
      <v-col cols="5">
        <v-row> 
          <v-col cols="12"><h5>스케줄 정보</h5></v-col>
          <v-col cols="12">{{ receive.schedule.overview }}</v-col>
          <v-col cols="12">{{ changeDateFormat(receive.schedule.start_date) }} ~ {{ changeDateFormat(receive.schedule.end_date) }}</v-col>
          <v-col cols="12" style="display: flex; justify-content: space-around;">
            <v-btn>최대 인원 : {{ receive.schedule.max_member }}</v-btn>
            <v-btn>{{ member_type[receive.schedule.member_type_pk] }}</v-btn>
            <v-btn>{{ style_type[receive.schedule.style_type_pk] }}</v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12"><h5>신청자 정보</h5></v-col>
          <v-col cols="3">
            <v-avatar>
              <img
                :src="
                  !!receive.user.profile_image
                    ? profileURL(receive.user)
                    : require(`@/assets/images/${receive.user.gender}.png`)
                "
                alt="profile_image"
              >
            </v-avatar>
          </v-col>
          <v-col cols="9">
            <v-row>{{ receive.user.nickname }}</v-row>
            <v-row>({{ receive.user.username }})</v-row>
          </v-col>
          <v-col cols="12">
            자기소개 : {{ receive.user.introduce }}
          </v-col>
          <v-col cols="12">
            신청 글 : {{ receive.content }}
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="2">
        <v-row style="display:flex; justify-content: center;" class="my-5">
          <v-btn color="primary" @click="approve(receive.id)">승인</v-btn>
        </v-row>
        <v-row style="display:flex; justify-content: center;" class="my-5">
          <v-btn color="error" @click="refuse(receive.id)">취소</v-btn>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'

import ScheduleCard from '@/components/schedules/ScheduleCard'

export default {
  name: 'ReceivedScheduleList',
  props: {
    receiveds: {
      type: Array,
    }
  },
  data() {
    return {
      member_type: [null, '혼자', '가족들', '친구들', '단체'],
      style_type: [null, '힐링', '액티비티', '맛집 탐방', '역사 탐방'],
    }
  },
  computed: {
    ...mapGetters('accounts', ['config']),
  },
  components: {
    ScheduleCard,
  },
  methods: {
    profileURL(user) {
      return process.env.VUE_APP_SERVER_URL + user.profile_image
    },
    changeDateFormat(date) {
      let temp_date = new Date(date).toISOString();
      return temp_date.slice(0, 10) + ' ' + temp_date.slice(11, 16)
    },
    approve(receive_id) {
      let response = confirm('승인하시겠습니까?')
      if (response) {
        let body = {
          user_schedule_pk: receive_id
        };
        axios.post(process.env.VUE_APP_SERVER_URL + '/join/confirm/', body, {
          headers: {
            Authorization: this.config
          }
        })
        .then(() => {
          alert('승인에 성공했습니다!');
          this.$emit('received');
        })
        .catch(err => console.log(err.response))
      }
    },
    refuse(receive_id) {
      let response = confirm('정말 거절할건가요?')
      if (response) {
        axios.delete(process.env.VUE_APP_SERVER_URL + '/join/' + receive_id + '/', {
          headers: {
            Authorization: this.config
          }
        })
        .then(() => {
          alert('거절에 성공했을 때 피드백 필요');
          this.$emit('received');
        })
        .catch(err => console.log(err.response))
      }
    },
  }
}
</script>

<style>

</style>