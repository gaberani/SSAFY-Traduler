<template>
	<v-container>
		<v-row>
      <v-col cols="2" offset="2">
        <v-avatar
          style="cursor: pointer; width: 10vw; height: 10vw;"
        >
          <img
            :src="
              !!userInfo.profile_image
                ? profileURL
                : require(`@/assets/images/${userInfo.gender}.png`)
            "
            alt="John"
          >
        </v-avatar>
      </v-col>
      <v-col cols="8">
        <h1>내 정보</h1>
        <p>{{ userInfo.nickname }} ({{ userInfo.username }})</p>

        <p v-if="userInfo.introduce">{{ userInfo.introduce }}</p>
        <p v-else>작성된 자기소개가 없습니다.</p>

        <v-row>
          <v-col cols="12">
            <v-btn @click="changeView('update')" style="margin-right: 1vw;">정보 수정</v-btn>
            <v-btn @click="changeView('favorite')" style="margin-right: 1vw;">즐겨찾기한 여행지</v-btn>
            <v-btn @click="changeView('written')" style="margin-right: 1vw;">작성한 스케줄</v-btn>
            <v-btn @click="changeView('joined')">참여한 스케줄</v-btn>
          </v-col>
          <v-col cols="12">
            <v-btn @click="changeView('received')" style="margin-right: 1vw;">받은 신청들</v-btn>
            <v-btn @click="changeView('invited')" style="margin-right: 1vw;">초대된 스케줄</v-btn>
            <v-btn @click="changeView('submit')">참가신청한 스케줄</v-btn>
          </v-col>
        </v-row>

      </v-col>
    </v-row>

    <v-row>
      <v-col cols="8" offset="2">

        <UserInfoUpdate v-if="viewMode == 'update'" :userInfo="userInfo" @updated="updateUserInfo"/>

        <div v-if="viewMode == 'favorite'">
          <div v-for="(favorite_spot, index) in spotDetails" :key="favorite_spot.id" style="display:inline;">
            <!-- v-for -->
            <SpotCard :spot="favorite_spot" @like="likeSpot(index)" @unlike="unlikeSpot(index)" />
          </div>

          <v-pagination
            v-model="curSpotPage"
            :length="spot_page.endPage"
            :total-visible="7"
            class="mt-5"
          ></v-pagination>
        </div>

        <v-row v-if="viewMode == 'written'">
          <v-col
            cols="4"
            style="display:inline-block; padding:6px;"
            v-for="written_schedule in written_schedules" :key="written_schedule.id"
          >
          <ScheduleCard :data="written_schedule.id" :schedule="written_schedule"/>
          </v-col>
          <v-col cols="12">
            <v-pagination
              v-model="curSchedulePage"
              :length="schedule_page.endPage"
              :total-visible="7"
              class="mt-5"
            ></v-pagination>
          </v-col>
        </v-row>
        
        <v-row v-if="viewMode == 'joined'">
          <v-col
            cols="4"
            style="display:inline-block; padding:6px;"
            v-for="joined_schedule in joined_schedules" :key="joined_schedule.id"
          >
          <ScheduleCard :data="joined_schedule.schedule.id" :schedule="joined_schedule.schedule"/>
          </v-col>
          <v-col cols="12">
            <v-pagination
              v-model="curJoinedSchedulePage"
              :length="joined_schedule_page.endPage"
              :total-visible="7"
              class="mt-5"
            ></v-pagination>
          </v-col>
        </v-row>

        <div v-if="viewMode == 'received'">
          <ReceivedScheduleList :receiveds=receiveds @received="received"/>
          
          <v-row style="display: flex; justify-content: center;">
            <v-pagination
              v-model="curReceivedPage"
              :length="received_page.endPage"
              :total-visible="7"
              class="mt-5"
            ></v-pagination>
          </v-row>
        </div>

        <div v-if="viewMode == 'invited'">
          <InvitedScheduleList :invitations=invitations @invited="invited" />
          
          <v-row style="display: flex; justify-content: center;">
            <v-pagination
              v-model="curInvitaionPage"
              :length="invitation_page.endPage"
              :total-visible="7"
              class="mt-5"
            ></v-pagination>
          </v-row>
        </div>
        
        <div v-if="viewMode == 'submit'">
          <SubmitList :submits=submits @submitted="submitted" />
          
          <v-row style="display: flex; justify-content: center;">
            <v-pagination
              v-model="curSubmitPage"
              :length="sibmit_page.endPage"
              :total-visible="7"
              class="mt-5"
            ></v-pagination>
          </v-row>
        </div>
      </v-col>
    </v-row>
	</v-container>
</template>

<script>
import axios from 'axios'
import { mapActions, mapGetters } from 'vuex'

import UserInfoUpdate from '@/components/accounts/UserInfoUpdate.vue'
import InvitedScheduleList from '@/components/accounts/InvitedScheduleList.vue'
import ReceivedScheduleList from '@/components/accounts/ReceivedScheduleList.vue'
import SubmitList from '@/components/accounts/SubmitList.vue'

import SpotCard from '@/components/spots/SpotCard.vue'
import ScheduleCard from '@/components/schedules/ScheduleCard.vue'

export default {
  name: 'UsersMypage',
  components: {
    UserInfoUpdate,
    SpotCard,
    ScheduleCard,
    InvitedScheduleList,
    ReceivedScheduleList,
    SubmitList
  },
	data() {
		return {
      viewMode: "update",
      userInfo: {
        age: 0,
        gender: "남성",
        introduce: "",
        nickname: "",
        profile_image: null,
        username: "",
      },
      curSpotPage: 1,
      favorite_spots: [],
      spot_page: {},

      curSchedulePage: 1,
      written_schedules: [],
      schedule_page: {},

      curJoinedSchedulePage: 1,
      joined_schedules: [],
      joined_schedule_page: {},

      curInvitaionPage: 1,
      invitations: [],
      invitation_page: {},

      curReceivedPage: 1,
      receiveds: [],
      received_page: {},

      curSubmitPage: 1,
      submits: [],
      sibmit_page: {},
		}
	},
  computed: {
    ...mapGetters('accounts', ["config"]),
    headers() {
      return {Authorization: this.config}
    },
    profileURL() {
      return process.env.VUE_APP_SERVER_URL + this.userInfo.profile_image
    },
    spotDetails() {
      let tempDetails = []
      this.favorite_spots.forEach(el => {
        let tempDetail = el.spot_detail;
        tempDetail['avg_score'] = el.avg_score;
        tempDetail['total_likes'] = el.total_likes;
        tempDetail['is_liked'] = el.is_liked;
        tempDetails.push(tempDetail);
      })
      return tempDetails
    }
  },
  watch: {
    curSpotPage() {
      this.getFavoriteSpots();
    },
    curSchedulePage() {
      this.getWrittenSchedules();
    },
    curJoinedSchedulePage() {
      this.getJoinedSchedule();
    },
    curInvitaionPage() {
      this.getInvitaions();
    },
    curReceivedPage() {
      this.getReceived();
    },
    curSubmitPage() {
      this.getSubmits();
    },
    viewMode() {
      this.getDetailInfo();
    }
  },
  methods: {
    ...mapActions('accounts', ["GetUserInfo"]),
    changeView(view) {
      this.viewMode = view;
    },
    getDetailInfo() {
      switch (this.viewMode) {
        case 'favorite' :
            this.getFavoriteSpots();
            break;
        case 'written' :
            this.getWrittenSchedules();
            break;
        case 'joined' :
            this.getJoinedSchedules();
            break;
        case 'received' :
            this.getReceived();
            break;
        case 'invited' :
            this.getInvitaions();
            break;
        case 'submit' :
            this.getSubmits();
            break;
        default :
            this.getUserInfo();
      }
    },
    updateUserInfo(updatedInfo) {
      this.userInfo.nickname = updatedInfo.nickname;
      this.userInfo.introduce = updatedInfo.introduce;
      this.userInfo.profile_image = updatedInfo.profile_image.slice(29);
      alert('유저 정보 수정에 성공했습니다!');
    },
    getUserInfo() {
      axios.get(process.env.VUE_APP_SERVER_URL + '/accounts/my_info/', {
        headers: this.headers,
      })
      .then(res => {
        this.userInfo = res.data.user;
      })
      .catch(err => console.log(err))
    },
    getFavoriteSpots() {
      axios.get(process.env.VUE_APP_SERVER_URL + '/accounts/favorite_spots', {
        headers: this.headers,
        params: {
          curSpotPage: this.curSpotPage,
        }
      })
      .then(res => {
        this.favorite_spots = res.data.favorite_spots;
        this.spot_page = res.data.spot_page;
      })
      .catch(err => console.log(err.response))
    },
    getWrittenSchedules() {
      axios.get(process.env.VUE_APP_SERVER_URL + '/accounts/written_schedules', {
        headers: this.headers,
        params: {
          curSchedulePage: this.curSchedulePage,
        }
      })
      .then(res => {
        this.written_schedules = res.data.written_schedules;
        this.schedule_page = res.data.schedule_page;
      })
      .catch(err => console.log(err.response))
    },
    getJoinedSchedules() {
      axios.get(process.env.VUE_APP_SERVER_URL + '/join/joined_schedules/', {
        headers: this.headers,
        params: {
          curPage: this.curJoinedSchedulePage,
        }
      })
      .then(res => {
        this.joined_schedules = res.data.schedule;
        this.joined_schedule_page = res.data.page;
      })
      .catch(err => console.log(err.response))
    },
    getInvitaions() {
      axios.get(process.env.VUE_APP_SERVER_URL + '/join/invitation/', {
        headers: this.headers,
        params: {
          curPage: this.curInvitaionPage,
        }
      })
      .then(res => { 
        this.invitations = res.data.invited_schedules;
        this.invitation_page = res.data.page;
      })
      .catch(err => console.log(err.response))
    },
    invited() {
      this.getInvitaions();
    },
    getReceived() {
      axios.get(process.env.VUE_APP_SERVER_URL + '/join/recieved_requests/', {
        headers: this.headers,
        params: {
          curPage: this.curReceivedPage,
        }
      })
      .then(res => {
        this.receiveds = res.data.schedule;
        this.received_page = res.data.page;
      })
      .catch(err => console.log(err.response))
    },
    received() {
      this.getReceived();
    },
    getSubmits() {
      axios.get(process.env.VUE_APP_SERVER_URL + '/join/requests/', {
        headers: this.headers,
        params: {
          curPage: this.curSubmitPage,
        }
      })
      .then(res => {
        this.submits = res.data.submit_requests;
        this.sibmit_page = res.data.page;
      })
      .catch(err => console.log(err))
    },
    submitted() {
      this.getSubmits();
    },
    likeSpot(index) {
      this.favorite_spots[index] = true;
    },
    unlikeSpot(index) {
      this.favorite_spots[index] = false;
    }
  },
  created() {
    this.getUserInfo();
  }
}
</script>

<style>

</style>