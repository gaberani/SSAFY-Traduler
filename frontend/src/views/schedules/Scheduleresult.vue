<template>
  <v-app>
      <SearchSchedule/>
      <SearchSDresult/>
      <Footer/>
  </v-app>
</template>

<script>
import SearchSchedule from '@/components/schedules/SearchSchedule';
import SearchSDresult from '@/components/schedules/SearchSDresult';
import Footer from '@/components/common/Footer';
export default {
    components:{SearchSchedule, SearchSDresult,Footer},
    name: 'Scheduleresult',
}
</script>

<style>

</style>