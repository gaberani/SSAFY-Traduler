
<template>
  <v-card flat tile>
    <v-toolbar id="navb">
        <img  style="height:70%;" src="@/assets/tradulerlogo.png" />
      <v-toolbar-title @click="gotoHome" style="font-family: 'jalnanregular'; font-size:1.5rem" class="headertitle">Traduler</v-toolbar-title>
      <v-spacer ></v-spacer>
        <v-btn text @click="gotoHome" class="navbar-btn">홈</v-btn>     
        <v-btn text @click="gotoSchedulemain" class="navbar-btn">스케쥴러</v-btn>    
        <v-btn text @click="gotoSpot" class="navbar-btn">여행지 검색</v-btn>     
        <v-btn v-if="!this.LoginFlag" text @click="gotoLogin" class="navbar-btn">로그인</v-btn>
        <div v-else>
          <v-btn text @click="gotoMypage" class="navbar-btn">마이페이지</v-btn>
          <v-btn text @click="SubmitLogout" class="navbar-btn">로그아웃</v-btn>
        </div>
    </v-toolbar>
  </v-card>
</template>


<script>
import { mapGetters, mapActions } from 'vuex'

export default {
    name: 'Header',
    methods: {
      ...mapActions(["SubmitLogout"]),
      gotoSpot() {
        this.$router.push("/spot")
      },
      gotoSchedulemain() {
        this.$router.push("/schedulemain")
      },
      gotoLogin() {
        this.$router.push({name:"UsersLogin"})
      },
      gotoHome() {
        this.$router.push({name:"Home"})
      },
      gotoMypage() {
        this.$router.push({name:"UsersMypage"})
      }
    },
    computed: {
      ...mapGetters(['LoginFlag'])
    }
}
</script>

<style>
@import url(../fonts/jalnan/stylesheet.css);

html, body {
  font-family:'jalnanregular';
}
h1, h2, h3, h4, h5, h6 {
  font-family: 'jalnanregular';
}
.navbar-btn {
  font-family: 'SCDream5'
}
.headertitle:hover{cursor: pointer; }
</style>