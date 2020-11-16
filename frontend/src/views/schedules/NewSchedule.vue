<template>
  <v-app>
      <SearchSchedule/>
      <NewScheduleplus/>
      <Footer/>
  </v-app>
</template>

<script>
import SearchSchedule from '@/components/schedules/SearchSchedule';
import NewScheduleplus from '@/components/schedules/NewScheduleplus';
import Footer from '@/components/common/Footer';
export default {
    components:{SearchSchedule,NewScheduleplus, Footer},
    name: 'NewSchedule',
}
</script>

<style>

</style>