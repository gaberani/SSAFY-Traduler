<template>
  <div class="img_block">
    <p class="error_text">
      찾을 수 없는 페이지입니다
    </p>
  </div>
</template>

<script>
export default {
  name: '404Page',

}
</script>

<style scoped>
.img_block {
    background-image : url("../assets/headers/test.jpg");
    background-size:cover;
    width:100%;
    min-height: 45vw;
}

.error_text {
  font-size: 3vw;
  font-family: 'SCDream9';
  font-weight: bolder;
  margin-top: 16.5vw;
  margin-left: 15vw;
  color: white;
}
</style>