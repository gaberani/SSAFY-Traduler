<template>
  <v-app>
    <Header/>
    <h1>Lorem Ipsum Dolor</h1>
    <h3>ㅎㅎㅎㅎㅎ</h3>
    <h2>강원도는 어때요?</h2>
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