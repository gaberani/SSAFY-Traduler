<template>
  <v-app>
    <Header/>
    <router-view :key="$route.fullPath"></router-view>
  </v-app>
</template>

<script>
import Header from '@/components/Header';
export default {
  name: 'App',

  components: {
    Header,
  },

  data: () => ({
    //
  }),
};
</script>

<style>
@import url(./fonts/jalnan/stylesheet.css);

html, body {
  font-family:'jalnanregular';
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'jalnanregular';
}
</style>