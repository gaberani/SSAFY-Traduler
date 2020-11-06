<template>
  <v-app>
      <SearchSchedule/>
      <SearchSDresult/>
      <Footer/>
  </v-app>
</template>

<script>
import SearchSchedule from '@/components/SearchSchedule';
import SearchSDresult from '@/components/SearchSDresult';
import Footer from '@/components/Footer';
export default {
    components:{SearchSchedule, SearchSDresult,Footer},
    name: 'SDresult',
}
</script>

<style>

</style>