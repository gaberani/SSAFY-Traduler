<template>
  <div class="home">
    <h1 style="text-align:center;">This is Home Page</h1>
    <v-btn
      @click="gotoMypage"
    >
      내 정보
    </v-btn>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
  },
  methods: {
    gotoMypage() {
      this.$router.push({name: 'UsersMypage'})
    }
  }
}
</script>
