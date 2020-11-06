<template>
  <v-app>
      <SearchSchedule/>
      <SDMainCenter/>
  </v-app>
</template>

<script>
import SearchSchedule from '@/components/SearchSchedule';
import SDMainCenter from '@/components/SDMainCenter';
export default {
    components:{SearchSchedule, SDMainCenter},
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