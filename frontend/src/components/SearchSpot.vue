<template>
<div class="spotimg">
    <div class="searchbox">
    <center>
    <select class="selectspot">
        <!-- v-model="" -->
        <option value="" >111</option>
        <option value="">222</option>
    </select>
    <select class="selectspot">
        <!-- v-model="" -->
        <option value="" >111</option>
        <option value="">222</option>
    </select>
    <div>
        <input class="spotsearch" placeholder="원하는 여행지를 입력하세요.">
        <button style="margin-left:-40px;"><i style="font-size:1.7vw" class="fas fa-search"></i></button>
    </div>
    </center>
    </div>
</div>
</template>

<script>
export default {

}
</script>

<style>
.spotimg {
    background-image : url("../assets/searchspot.jpg");
    background-size:cover;
    width:100%;
    min-height: 43%;
}
.spotsearch {
    width:40%;
    height:50px;
    background-color:white;
    border:3px #EB7878 solid;
    border-radius:50px;
    outline:none;
    padding-left: 15px;
    margin-top:10px;
    font-size:1.2vw;
}
.selectspot {
    height:5%;
    width:10%;
    background-color:white;
    border:3px #EB7878 solid;
    margin:1px;
    outline:none;
    appearance: button;
    font-size:1.2vw;
}
.searchbox {
    margin-top:20%
}
.spotsearch:focus::-webkit-input-placeholder { /* WebKit browsers */ color:transparent; }

</style>