<template>
  <v-app class="home">
    <Mainimage/>
    <MainCenter/>
    <Footer/>
  </v-app>
</template>

<script>

import Mainimage from '@/components/common/Mainimage';
import MainCenter from '@/components/common/MainCenter';
import Footer from '@/components/common/Footer';
export default {
  name: 'Home',
  components: {
    Mainimage,
    MainCenter, 
    Footer
  },
  methods: {
    gotoMypage() {
      this.$router.push({name: 'UsersMypage'})
    }
  }
}
</script>
