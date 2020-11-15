<template >
  <v-dialog
    v-model="dialog"
    max-width="60%"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-card
        class="spotcard"
        width="31.333333%"
        height="30vh 30vw"
      >
        <v-img
          :src="spot.image"
          v-bind="attrs"
          v-on="on"
          class="imgbtn"
          lazy-src="@/assets/images/lazy-loading.jpg"
        >
          <template v-slot:placeholder>
            <lazy-loading />
          </template>
          <button style="margin-left:84%; margin-top:3%; outline:none;">
          <!-- 아이콘 바꾸기 -->
            <i class="fas fa-star" v-if="spot.is_liked==true" @click.stop="unlikespot" style="font-size:1.8vw; color:#FFDF00;"></i>
            <i class="fas fa-star" v-else @click.stop="likespot" style="font-size:1.8vw; color:black;"></i>
          </button>
        </v-img>

        <v-card-title class="cardtitle" v-bind="attrs" v-on="on" >
          <p v-bind="attrs" v-on="on" class="titlebtn">{{spot.title}}</p>
        </v-card-title>

        <v-card-subtitle class="cardcontent">
          {{spot.address}}
        </v-card-subtitle>
      </v-card>
    </template>

    <!-- modal -->
    <v-card style="border-radius:15px;">
      <div class="modalheader">
        <v-card-title class="modaltitle">{{spot.title}}</v-card-title>
        <v-btn
          color="blue darken-1"
          text
          @click="dialog = false"
          class="modalclose"
        >
          <i class="fas fa-times" style="font-size:1.5rem; color:white;"></i>
        </v-btn>
      </div>

      <v-divider style="background-color:#FF5E5E;"></v-divider>

      <div class="modalbody" style="height: 30vw;">
        <v-container>
          <v-row>
            <v-col cols="6">
              <v-img :src="spot.image" height="21vw" />
            </v-col>
            <v-col cols="6">
              <SpotDetailMap :lat="spot.lat" :lon="spot.lon" :item="spot.id"/>
              <p style="text-align: center; font-size: 1vw; margin-top:1vw">{{ spot.address }}</p>
            </v-col>
          </v-row>
          <v-row class="modal-footer">

            <v-col cols="2" offset="2">
              <v-btn
                depressed
                v-if="spot.is_liked==true"
                @click.stop="unlikespot" 
              >
                <div>
                  <v-icon color="red">mdi-heart</v-icon>{{ spot.total_likes }}
                </div>
              </v-btn>
              <v-btn
                depressed
                v-else
                @click.stop="likespot"
              >
                <div>
                  <v-icon>mdi-heart</v-icon>{{ spot.total_likes }}
                </div>
              </v-btn>
            </v-col>

            <v-col cols="4">
              <v-rating
                v-model="spot.avg_score"
                color="yellow darken-3"
                background-color="grey darken-1"
                empty-icon="$ratingFull"
                readonly
                half-increments
                hover
                large
              ></v-rating>
            </v-col>

            <v-col cols="2">
              <router-link :to="{name: 'SpotDetail', params: {spot_id: spot.id} }" style="text-decoration: none;"><v-btn color='error' depressed>상세보기</v-btn></router-link>
            </v-col>

          </v-row>
        </v-container>
      </div>
    </v-card>
  </v-dialog>
  <!-- </v-card> -->
</template>

<script>
  import axios from 'axios'
  import { mapGetters } from "vuex";

  import SERVER from '@/api/api'

  import SpotDetailMap from '@/components/spots/SpotDetailMap'

  export default {
    props: {
      spot: {
        type: Object,
      },
    },
    data () {
      return {
        dialogm1: '',
        dialog: false,
        detailspot: [],
        spotcomments: [],
        score: 0,
        content: "",
        page: 1,
        detailpage: [],
        testScore: 0,
      }
    },
    components: {
      SpotDetailMap,
    },
    computed: {
      ...mapGetters('accounts', ["LoginFlag", "config", "userInfo"]),
      headers() {
        return (this.LoginFlag ? {headers: {Authorization: this.config}} : null)
      },
      username() {
        return sessionStorage.getItem("username");
      }
    },
    methods: {
      likespot() {
        if (!this.LoginFlag) {
          let response = confirm('로그인이 필요한 기능입니다!\n\n로그인 페이지로 이동하시겠습니까?')
          if (response) {
            this.$router.push({name: 'UsersLogin'})
          }
        } else {
          axios.post(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.SPOTS + this.spot.id + SERVER.URL.SPOT.LIKE, null, this.headers)
          .then(() => {
            this.spot.is_liked = true;
            this.spot.total_likes += 1;
            this.$emit('like')
          })
          .catch(err => console.log(err.response))
        }
      },
      unlikespot() {
        if (!this.LoginFlag) {
          let response = confirm('로그인이 필요한 기능입니다!\n\n로그인 페이지로 이동하시겠습니까?')
          if (response) {
            this.$router.push({name: 'UsersLogin'})
          }
        } else {
          axios.delete(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.SPOTS + this.spot.id + SERVER.URL.SPOT.LIKE, this.headers)
          .then(() => {
            this.spot.is_liked = false;
            this.spot.total_likes -= 1;
            this.$emit('unlike')
          })
          .catch(err => console.log(err.response))
        }
      },
    },
  }
</script>

<style scoped>
  .cardtitle {
    font-size:1vw;
    margin-top:0.5%;
    margin-left:2%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    padding:0;
    display:inline-block;
    font-family: 'SCDream7'
  }
  .v-application p {
    margin-bottom: 3px;
  }
  .cardcontent {
    margin-left:2%;
    font-size:0.8vh;
    overflow: hidden;
    text-overflow: ellipsis;
    padding:0;
    white-space: nowrap;
    font-family: 'SCDream4'
  }
  .spotcard {
    display:inline-block;
    margin-left:1%;
    margin-right:1%;
    margin-bottom:2%;
  }
  .titlebtn {
    outline:none;
  }
  .titlebtn:hover{
    background-color:rgb(224, 224, 224);
  }
  .imgbtn {
    max-width:100%;
    /* max-height:; */
    /* max-height:75%; */
    height:30vh;
  }
  .imgbtn:hover{
    cursor: pointer;
  }
  .modalclose {
    float:right;
  }
  .modaltitle {
    display:inline;
    color:white;
    font-family: 'SCDream5';
    font-size:1.2vw;
  }
  .modalheader {
    background-color:#FF5E5E;
    width:100%;
  }
  .modalimg {
    width:55%;
    display:inline-block;
  }
  .modaldetail {
    width:45%;
    display:inline-block;
    height:20vw;
    overflow: auto;
  }
  .modalcomment {
    margin-top:15px;
  }
  .modalinput {
    border: 2px #FF5E5E solid;
    margin-left:10px;
    font-family: 'SCDream4';
    border-radius: 15px;
    outline:none;
    padding-left: 12px;
  }
  .commentbtn {
    background-color:  #FF5E5E;
    height: 30px;
    width: 50px;
    color:white;
    border-radius: 10px;
    margin-left:10px;
    font-family: 'SCDream4'
  }
  .commentbdg {
    display: inline-block;
    text-align:center;
    font-size:1rem;
    background-color:#1793FF;
    color:white;
    height:22px;
    width:25px;
    border-radius:12px;
    margin-right: 18px;
    font-family: 'SCDream5'
  }
  .detailplus {
    width:70px;
    height:30px;
    border-radius:20px;
    background-color: #FF5E5E;
    color:white;
    outline:none;
    font-family: 'SCDream6'
  }
  .selectrate {
    border:2px #FF5E5E solid;
    appearance: button;
    font-size:1rem;
    margin-left:10px;
    width: 35px;
    font-family: 'SCDream4';
    border-radius: 15px;
    outline:none;
  }
  /* 스크롤 바 넓이 16px */
  .modaldetail::-webkit-scrollbar{
    width: 16px;
  }
  /* 스크롤 바 기본 색상 */
  .modaldetail::-webkit-scrollbar-track {background-color:#FF5E5E;
    box-shadow: inset 0px 0px 5px white;
    border-radius: 10px;
  }
  /* 스크롤 구간 배경 색상 */
  .modaldetail::-webkit-scrollbar-thumb {background-color:#ff9a9a;
    border-radius: 10px;
  } 
  /* 스크롤 바 위에 마우스 올렸을 때(hover) 색상 */
  .modaldetail::-webkit-scrollbar-thumb:hover {
    background-color: #fd4b4b;
  }
  .modal-footer {
    align-items: center;
  }
</style>