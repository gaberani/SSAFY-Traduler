<template>
  <v-app>
    <SearchSpot/>
    <SpotList/>
  </v-app>
</template>

<script>
import SearchSpot from '@/components/SearchSpot';
import SpotList from '@/components/SpotList';
export default {
    components:{SearchSpot, SpotList}
}
</script>

<style>

</style>