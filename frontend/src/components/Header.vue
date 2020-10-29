
<template>
  <v-card
    flat
    tile
  >
    <v-toolbar id="navb">
        <img  style="height:70%;" src="@/assets/tradulerlogo.png" />
      <v-toolbar-title style="font-family: 'jalnanregular'; font-size:1.5rem">Traduler</v-toolbar-title>
      <v-spacer ></v-spacer>
        <v-btn text @click="gotoHome" style="font-family: 'SCDream5'">홈</v-btn>     
        <v-btn text style="font-family: 'SCDream5'">스케쥴러</v-btn>    
        <v-btn text @click="gotoSpot" style="font-family: 'SCDream5'">여행지 검색</v-btn>     
        <v-btn text @click="gotoLogin" style="font-family: 'SCDream5'">로그인</v-btn>     
        
    </v-toolbar>
  </v-card>
</template>


<script>
export default {
    name: 'Header',
    methods: {
      gotoSpot() {
        this.$router.push("/spot")
      },
      gotoLogin() {
        this.$router.push({name:"Login"})
      },
      gotoHome() {
        this.$router.push({name:"Home"})
      }
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
</style>