
<template>
  <v-card flat tile>
    <v-toolbar id="navb">
        <img  style="height:70%;" src="@/assets/tradulerlogo.png" />
      <v-toolbar-title style="font-family: 'jalnanregular'; font-size:1.5rem" class="headertitle"><router-link :to="{name: 'Home'}" class="nav-btn" style="color: #ff5e5e;">Traduler</router-link></v-toolbar-title>
      <v-spacer ></v-spacer>
        <router-link :to="{name: 'Home'}" class="nav-btn"><v-btn text class="navbar-btn">홈</v-btn></router-link>
        <router-link :to="{name: 'ScheduleMain'}" class="nav-btn"><v-btn text class="navbar-btn">스케줄러</v-btn></router-link>
        <router-link :to="{name: 'SpotMain'}" class="nav-btn"><v-btn text class="navbar-btn">여행지 검색</v-btn></router-link>

        <router-link v-if="!this.LoginFlag" :to="{name: 'UsersLogin'}" class="nav-btn"><v-btn text class="navbar-btn">로그인</v-btn></router-link>
        <div v-else>
          <router-link :to="{name: 'UsersMypage'}" class="nav-btn"><v-btn text class="navbar-btn">마이페이지</v-btn></router-link>
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
      ...mapActions('accounts', ["SubmitLogout"]),
    },
    computed: {
      ...mapGetters('accounts', ['LoginFlag'])
    }
}
</script>

<style>
@import url(../../fonts/jalnan/stylesheet.css);

html, body {
  font-family:'jalnanregular';
}
h1, h2, h3, h4, h5, h6 {
  font-family: 'jalnanregular';
}
.nav-btn {
  text-decoration: none;
}
.navbar-btn {
  font-family: 'SCDream5'
}
.headertitle:hover{cursor: pointer; }
</style>