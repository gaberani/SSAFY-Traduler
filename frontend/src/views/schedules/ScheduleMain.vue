<template>
  <v-app>
      <SearchSchedule/>
      <SDMainCenter/>
      <Footer/>
  </v-app>
</template>

<script>
import SearchSchedule from '@/components/schedules/SearchSchedule';
import SDMainCenter from '@/components/schedules/SDMainCenter';
import Footer from '@/components/common/Footer';
export default {
    components:{SearchSchedule, SDMainCenter, Footer},
    name: 'ScheduleMain',
	data() {
		return {
			
		}
	},
	methods: {

	}
}
</script>

<style>

</style>