<template>
  <div class="spotlist">
      <div>
        <h4>현재 작성중인 여행지</h4>
      <!-- 리스트 나중에 -->
      </div>
      <div>
        <div class="mb-3 mt-3">
            <!-- 경상도부분 나중에 랜덤으로 -->
            <h1 style="display:inline; color:#FF5E5E">경상도</h1>
            <h3 style="display:inline; ">는 어때요?</h3>
            <button class="plusbtn">더보기</button>
        </div>
        <div >
            <!-- v-for -->
            <SpotCard/>
            <SpotCard/>
            <SpotCard/>
        </div>
      </div>
      <div>
        <div class="mb-3 mt-2">
            <h1 style="display:inline; color:#FF9617">BEST</h1>
            <h3 style="display:inline; ">여행지</h3>
            <button class="plusbtn">더보기</button>
        </div>
        <div >
            <!-- v-for -->
            <SpotCard/>
            <SpotCard/>
            <SpotCard/>
        </div>
      </div>
  </div>
</template>

<script>
import SpotCard from '@/components/SpotCard';
export default {
    components:{SpotCard}

}
</script>

<style>
.spotlist {
    margin-top: 2%;
    width:66.6666666%;
    margin-left:16.6666666%;
}
.plusbtn {
    float:right;
    width:70px;
    height:40px;
    border-radius:20px;
    background-color: #FF5E5E;
    color:white;
    outline:none;
    font-family: 'SCDream6'
}
</style>