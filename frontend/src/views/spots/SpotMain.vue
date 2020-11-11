<template>
  <v-app>
    <SearchSpot/>
    <SpotList/>
    <Footer/>
  </v-app>
</template>

<script>
import SearchSpot from '@/components/spots/SearchSpot';
import SpotList from '@/components/spots/SpotList';
import Footer from '@/components/Footer';
export default {
    components:{SearchSpot, SpotList, Footer}
}
</script>

<style>

</style>