<template>
<div class="mainimg">
    <div class="maincontent">
        <center>
            <h1 style="color:white; font-size:2.5vw;">국내 여행엔 Traduler!</h1>
            <p class="mainp">OOOOO개의 여행지 데이터를 활용한 </p>
            <p class="mainp">추천과 스케쥴러를 사용해</p>
            <p class="mainp">여행을 계획해보세요!</p>
            <button class="mainbtn">Traduler 시작</button>
        </center>
    </div>
</div>
</template>

<script>
export default {
    data() {
      return {
      }
    },
    methods: {


    },
}
</script>

<style>
.mainimg {
    background-image : url("../../assets/mainimage.jpg");
    background-size:cover;
    width:100%;
    min-height: 35vw;
    background-position: center;
    filter:saturate(150%);
}
.maincontent {
    float:right;
    margin-top:7%;
    margin-right:15%;
}
.mainp {
    color:white;
    font-size:1.2vw;
    font-family: 'SCDream4'
}
.mainbtn {
    font-family: 'SCDream8';
    color:white;
    font-size:1.4vw;
    width:55%;
    height:3vw;
    background-color: rgba( 255, 19, 19, 0.55 );
    border-radius:25px;
}
</style>