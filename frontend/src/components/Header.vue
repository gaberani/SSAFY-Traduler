
<template>
  <v-card
    flat
    tile
  >
    <v-toolbar id="navb">
        <img  style="height:70%;" src="@/assets/tradulerlogo.png" />
      <v-toolbar-title style="font-family: 'jalnanregular'; font-size:1.5rem">Traduler</v-toolbar-title>
      <v-spacer ></v-spacer>
        <v-btn text @click="gotoHome" class="navbar-btn">홈</v-btn>     
        <v-btn text class="navbar-btn">스케쥴러</v-btn>    
        <v-btn text @click="gotoSpot" class="navbar-btn">여행지 검색</v-btn>     
        <v-btn v-if="!this.LoginFlag" text @click="gotoLogin" class="navbar-btn">로그인</v-btn>
        <v-btn v-else text @click="SubmitLogout" class="navbar-btn">로그아웃</v-btn>
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
      gotoLogin() {
        this.$router.push({name:"Login"})
      },
      gotoHome() {
        this.$router.push({name:"Home"})
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
</style>