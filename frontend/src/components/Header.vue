
<template>
  <v-card
    flat
    tile
  >
    <v-toolbar id="navb">
      <img  style="height:70%;" src="@/assets/tradulerlogo.png" />
      <v-toolbar-title>Traduler</v-toolbar-title>
      <v-spacer ></v-spacer>
      <v-btn text>홈</v-btn>     
      <v-btn text>스케쥴러</v-btn>    
      <v-btn text @click="gotoSpot">여행지 검색</v-btn>     
      <v-btn text @click="gotoLogin">로그인</v-btn>     
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
      }
    }
}
</script>

<style>

</style>