<template>
  <div class="spotimg">
    <div class="searchbox">
      <center>
        <select class="selectspot" v-model="area_code">
          <!-- v-model="" -->
          <option value="">지역</option>
          <option value="A">서울</option>
          <option value="B">인천</option>
          <option value="C">대전</option>
          <option value="D">대구</option>
          <option value="E">광주</option>
          <option value="F">부산</option>
          <option value="G">울산</option>
          <option value="H">세종</option>
          <option value="I">경기도</option>
          <option value="J">강원도</option>
          <option value="K">충청북도</option>
          <option value="L">충청남도</option>
          <option value="M">경상북도</option>
          <option value="N">경상남도</option>
          <option value="O">전라북도</option>
          <option value="P">전라남도</option>
          <option value="Q">제주도</option>
        </select>
        <select class="selectcategory" v-model="category_code">
          <!-- v-model="" -->
          <option value="" >카테고리</option>
          <option value="A01" >자연</option>
          <option value="A02" >인문(문화/예술/역사)</option>
          <option value="A03" >레포츠</option>
          <option value="A04" >쇼핑</option>
          <option value="A05" >음식</option>
          <option value="B01" >교통</option>
          <option value="B02" >숙박</option>
          <option value="C01" >추천코스</option>
        </select>
        <div>
          <input v-model="query" @keydown.enter="searchspots" class="spotsearch" placeholder="원하는 여행지를 입력하세요.">
          <button @click.prevent="searchspots" style="margin-left:-40px;"><i style="font-size:1.7vw" class="fas fa-search"></i></button>
        </div>
      </center>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        category_code: '',
        area_code: '',
        query: '',
      }
    },
    methods: {
      searchspots() {
          // this.$router.push("/spot/search?title=" + this.query 
          // + "&category=" + this.category_code + "&area=" + this.area_code + "&curPage=1")
          this.$router.push({ name: 'SpotSearch', query: {
            title: this.query,
            category: this.category_code,
            area: this.area_code,
            curPage: 1
          }
        })
      }
    },
  }
</script>

<style scoped>
.spotimg {
    background-image : url("../../assets/headers/spots.jpg");
    background-size:cover;
    width:100%;
    min-height: 35vw;
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
    font-family: 'SCDream5'
}
.selectspot {
    height:5%;
    width:7%;
    background-color:white;
    border:3px #EB7878 solid;
    margin:1px;
    outline:none;
    appearance: button;
    font-size:1.2vw;
    color: #EB7878;
    font-family: 'SCDream5'
}
.selectcategory {
    height:5%;
    width:14%;
    background-color:white;
    border:3px #EB7878 solid;
    margin:1px;
    outline:none;
    appearance: button;
    font-size:1.2vw;
    color: #EB7878;
    font-family: 'SCDream5'
}
.searchbox {
    margin-top:40vh;
}
.spotsearch::placeholder {
    color:#EB7878;
}
.spotsearch:focus::-webkit-input-placeholder { /* WebKit browsers */ color:transparent; }

</style>