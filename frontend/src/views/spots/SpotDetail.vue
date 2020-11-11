<template >
  <v-app>
    <div class="spotimg"
      v-bind:style="{ 'background-image': 'linear-gradient( rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4) ), url(' + spot.image + ')' }"
    >
      <h1 class="spot-title">{{ spot.title }}</h1>
      <div
        class="spot_scores">
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
        <v-btn
          depressed
          color="blue-grey lighten-4"
          style="margin-left: 5vw;"
          v-if="spot.is_liked==true"
          @click.stop="unlikespot" 
        >
          <div>
            <v-icon color="yellow">mdi-star</v-icon>{{ spot.total_likes }}
          </div>
        </v-btn>
        <v-btn
          depressed
          color="blue-grey lighten-4"
          style="margin-left: 5vw;"
          v-else
          @click.stop="likespot" 
        >
          <div>
            <v-icon>mdi-star</v-icon>{{ spot.total_likes }}
          </div>
        </v-btn>
      </div>
    </div>

    <v-container>
      <v-row style="margin-top: 3vw;">
        <v-col cols="4" offset="1">
          <SpotDetailMap :lat="spot.lat" :lon="spot.lon" :item="spot.id" /> 
        </v-col>
        <v-col cols="6" offset="1">
          <h3 class="spot-infos">{{ spot.title }}</h3>
          <h3 class="spot-infos">{{ area_name }} / {{ category_name }}</h3>
          <h3 v-if="spot.tel != null" class="spot-infos">{{ spot.tel }} / {{ spot.tel_name }}</h3>
          <h3 class="spot-infos">평균 평점 : {{ spot.avg_score }} 점</h3>
          <h3 class="spot-infos">즐겨찾기한 유저 수 : {{ spot.total_likes }}</h3>
        </v-col>
      </v-row>
      <v-row style="margin-top: 3vw;">
        <v-col cols="10" offset="1">
          <p v-html="spot.overview" />
        </v-col>
      </v-row>
      <v-row style="margin-top: 5vw;">
        <v-col cols="1" offset="1">
          <select class="selectrate" v-model="score" >
            <!-- v-model="" -->
            <option value="5">5</option>
            <option value="4">4</option>
            <option value="3">3</option>
            <option value="2">2</option>
            <option value="1">1</option>
          </select>
        </v-col>
        <v-col cols="7" offset="1">
          <input class="commentinput" style="width:70%;" v-model="content" @keydown.enter="writecomment" placeholder="댓글을 입력해주세요.">
        </v-col>
        <v-col cols="2">
          <button @click="writecomment" class="commentbtn">작성</button>
        </v-col>
      </v-row>
      <v-row style="margin-top: 2vw;" v-for="(comment, index) in spotcomments" :key="index">
        <v-col cols="2" offset="1" style="text-align: center;">
          <span class="commentbdg">{{comment.score}}</span>
        </v-col>
        
        <v-col cols="6">
          <span style="font-family: 'SCDream4'" >{{comment.content}}</span>
        </v-col>

        <v-col cols="3" class="d-flex" style="flex-direction: column;">
          <button v-if="username == comment.user.username" @click="deleteComment(comment.id,index)" style="margin-left:2%;" ><i class="far fa-times-circle" style="color:red;"></i></button>
          <span style="font-family: 'SCDream6'; float:right; margin-right:18%;">{{comment.user.nickname}} ({{ dateForm(comment.reg_time) }})</span>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4" offset="4">
          <v-pagination
            class="commentpage"
            v-model="page"
            :length="pageInfo.endPage"
            :total-visible="3"
            circle
          ></v-pagination>
        </v-col>
      </v-row>
    </v-container>
       
  </v-app>
  <!-- </v-card> -->
</template>

<script>
  import axios from 'axios'
  import { mapGetters } from "vuex";

  import SERVER from '@/api/api'
  import code_dict from '@/assets/code_dict.js'

  import SpotDetailMap from '@/components/spots/SpotDetailMap'

  export default {
    name: "SpotDetail",
    data () {
      return {
        dialogm1: '',
        dialog: false,
        spot: {
          address: "",
          area_code: "",
          category_code: "",
          content_type_pk: 0,
          id: 0,
          image: "",
          is_liked: false,
          lat: 0.0,
          lon: 0.0,
          overview: "",
          tel: null,
          tel_name: null,
          title: "",
          avg_score: 0,
          totla_likes: 0,
        },
        spotcomments: [],
        score: 5,
        content: "",
        page: 1,
        pageInfo: [],
      }
    },
    components: {
      SpotDetailMap
    },
    computed: {
      ...mapGetters(["LoginFlag", "config", "userInfo"]),
      headers() {
        return (this.LoginFlag ? {headers: {Authorization: this.config}} : null)
      },
      username() {
        return sessionStorage.getItem("username");
      },
      area_name() {
        return code_dict['area_dict'][this.spot.area_code]
      },
      category_name() {
        return code_dict['category_dict'][this.spot.category_code]
      }
    },
    methods: {
      dateForm(date) {
        return date.slice(0, 10)
      },
      likespot() {
        axios.post(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.SPOTS + this.spot.id + SERVER.URL.SPOT.LIKE, null, this.headers)
        .then(() => {
          this.spot.is_liked = true;
          this.spot.total_likes += 1;
        })
        .catch(err => console.log(err.response))
      },
      unlikespot() {
        axios.delete(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.SPOTS + this.spot.id + SERVER.URL.SPOT.LIKE, this.headers)
        .then(() => {
          this.spot.is_liked = false;
          this.spot.total_likes -= 1;
        })
        .catch(err => console.log(err.response))
      },
      writecomment() {
        let newComment = new FormData();
        newComment.append('spot_pk', this.spot.id);
        newComment.append('score', this.score);
        newComment.append('content', this.content);
        
        axios.post(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.COMMNET, newComment, this.headers)
        .then(({data}) => {
          this.spotcomments.unshift(data);
          this.content = '';
          this.score = 5;
        })
        .catch(err => {
          if (err.response.status == 400) {
            alert('빈 항목을 채워주세요!');
          }
        })
      },
      deleteComment(commentid, index) {
        axios.delete(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.COMMNET + commentid, this.headers)
        .then(() => {
          this.spotcomments.splice(index,1);
        })
        .catch(err => console.log(err.response))
      }
    },
    watch: {
      page() {
        axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.SPOTS + this.spot.id, {
          params: {
            curPage: this.page
          }
        })
        .then(response => {
          this.spotcomments = response.data.comments;
        })
        .catch(error => console.log(error))
      }
    },
    created () {
      axios.get(process.env.VUE_APP_SERVER_URL + SERVER.URL.SPOT.SPOTS + this.$route.params.spot_id, this.headers)
      .then(response => {
        let spotDetail = response.data
        this.spot = spotDetail.spot
        this.spotcomments = spotDetail.comments;
        this.pageInfo = spotDetail.page;
      })
      .catch(error => console.log(error))
    },
  }
</script>

<style scoped>
  .spot_scores {
    display: flex;
    justify-content: center;
    margin-top: 5vw;
    align-items: center;
  }

  .spotimg {
    background-size: cover;
    width: 100%;
    min-height: 45vw;
    filter:saturate(150%);
    padding: 18vw;
  }

  .spot-title {
    color: white;
    font-size: 3vw;
    text-align: center;
  }

  .spot-infos {
    margin-top: 1vw;
  }

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
  .commentinput {
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
    width: 100%;
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
</style>