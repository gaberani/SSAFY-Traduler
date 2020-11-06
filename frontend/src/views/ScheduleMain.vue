<template>
  <v-app>
      <SearchSchedule/>
      <SDMainCenter/>
      <Footer/>
  </v-app>
</template>

<script>
import SearchSchedule from '@/components/SearchSchedule';
import SDMainCenter from '@/components/SDMainCenter';
import Footer from '@/components/Footer';
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