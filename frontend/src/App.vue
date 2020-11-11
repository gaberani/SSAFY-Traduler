<template>
  <v-app>
    <Header/>
    <router-view :key="$route.fullPath"></router-view>
  </v-app>
</template>

<script>
import Header from '@/components/common/Header';
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
@import url(./fonts/SCDream/stylesheet.css);

html, body, .change-title-font {
  font-family:'jalnanregular';
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'jalnanregular';
}

p {
  font-family: 'SCDream3'
};
</style>