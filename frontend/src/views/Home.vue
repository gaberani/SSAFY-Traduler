<template>
  <v-app class="home">
    <Mainimage/>
    <MainCenter/>
    <Footer/>
  </v-app>
</template>

<script>

import Mainimage from '@/components/Mainimage';
import MainCenter from '@/components/MainCenter';
import Footer from '@/components/Footer';
export default {
  name: 'Home',
  components: {
    Mainimage,
    MainCenter, 
    Footer
  },
  methods: {
    gotoMypage() {
      this.$router.push({name: 'Mypage'})
    }
  }
}
</script>
