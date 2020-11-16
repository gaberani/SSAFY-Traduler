<template>
  <div>
    <div class="spotimg">
      <div class="spotmessage">
        <p style="margin-bottom:3px; font-family: 'SCDream8';">당신이 찾는 그 곳,</p>
        <p style="font-family: 'SCDream8';">Traduler와 떠나세요</p>
      </div>
    </div>
    <v-row no-gutters>
      <v-col
        cols="12"
        sm="2"
      >
      </v-col>
      <v-col
        cols="12"
        sm="8"
      >
        <div style="margin-top:35px; padding:5px; background-color: #ffc5c5; border: 5px solid #ffc5c5; border-radius:5px;">
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
        <input class="spotsearch" @keydown.enter="searchspots" placeholder="원하는 여행지를 입력하세요." v-model="query">
        <button @click.prevent="searchspots" class="searchbtn" ><i style="font-size:1.4vw" class="fas fa-search"></i></button>
      </div>
      </v-col>
      <v-col
        cols="12"
        sm="2"
      >
      </v-col>
    </v-row>
    <!-- <center>
      <hr style="margin-top:16px; width:66.6%; background-color:#FF5E5E;">
    </center> -->
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
    width:63%;
    height:38px;
    background-color:white;
    border:3px #EB7878 solid;
    border-radius:50px;
    outline:none;
    padding-left: 15px;
    margin-top:10px;
    font-size:1.2vw;
    font-family: 'SCDream5'
}
.spotsearch::placeholder {
  color:#EB7878;
}
.selectspot {
    height:30px;
    min-width:46px;
    width:9%;
    background-color:#EB7878;
    border:2px #EB7878 solid;
    outline:none;
    appearance: button;
    font-size:0.9vw;
    color: white;
    font-family: 'SCDream5';
    margin-right:10px;
}
.selectcategory {
    height:30px;
    min-width:46px;
    width:16%;
    background-color:#EB7878;
    border:2px #EB7878 solid;
    outline:none;
    appearance: button;
    font-size:0.9vw;
    color: white;
    font-family: 'SCDream5';
    margin-right:10px;
}
.spotmessage {
  font-weight: 900;
  color:white;
  position: absolute;
  font-family: 'SCDream9';
  margin-top:23vw;
  margin-left: 15%;
  font-size:3vw;
}
.spotsearch:focus::-webkit-input-placeholder { /* WebKit browsers */ color:transparent; }
.searchbtn {
    background-color:#EB7878;
    width:8%;
    height:38px;
    margin-bottom:2px;
    outline:none;
    min-width:50px;
    border-top:3px #EB7878 solid;
    border-radius:50px;
    color:white;
    margin-left:3px;
}
</style>