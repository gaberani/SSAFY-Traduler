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
    <v-row v-for="submit in submits" :key="submit.id" style="border-bottom: 1px solid black;">
      <v-col cols="5">
        <ScheduleCard :data="submit.id" :schedule="submit.schedule" />
      </v-col>
      <v-col cols="5">
        <v-row> 
          <v-col cols="12"><h5>스케줄 정보</h5></v-col>
          <v-col cols="12">{{ submit.schedule.overview }}</v-col>
          <v-col cols="12">{{ changeDateFormat(submit.schedule.start_date) }} ~ {{ changeDateFormat(submit.schedule.end_date) }}</v-col>
          <v-col cols="12" style="display: flex; justify-content: space-around;">
            <v-btn>최대 인원 : {{ submit.schedule.max_member }}</v-btn>
            <v-btn>{{ member_type[submit.schedule.member_type_pk] }}</v-btn>
            <v-btn>{{ style_type[submit.schedule.style_type_pk] }}</v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12"><h5>호스트 정보</h5></v-col>
          <v-col cols="3">
            <v-avatar>
              <img
                :src="
                  !!submit.user.profile_image
                    ? profileURL(submit.user)
                    : require(`@/assets/images/${submit.user.gender}.png`)
                "
                alt="profile_image"
              >
            </v-avatar>
          </v-col>
          <v-col cols="9">
            <v-row>{{ submit.user.nickname }}</v-row>
            <v-row>({{ submit.user.username }})</v-row>
          </v-col>
          <v-col cols="12">
            자기소개 : {{ submit.user.introduce }}
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="2">
        <v-row style="display:flex; justify-content: center;" class="my-5">
          <v-btn color="error" @click="refuse(submit.id)">취소</v-btn>
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
  name: 'SubmitList',
  props: {
    submits: {
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
    refuse(submit_id) {
      let response = confirm('정말 거절할건가요?')
      if (response) {
        axios.delete(process.env.VUE_APP_SERVER_URL + '/join/' + submit_id + '/', {
          headers: {
            Authorization: this.config
          }
        })
        .then(() => {
          alert('거절에 성공했을 때 피드백 필요');
          this.$emit('submitted');
        })
        .catch(err => console.log(err.response))
      }
    },
  }
}
</script>

<style>

</style>