<template>
  <div class="maincenter">
      <div>
        <div class="mb-3 mt-3">
            <h1 style="display:inline; color:#FF5E5E; font-size:2.7vw;">함께 </h1>
            <h3 style="display:inline; font-size:1.7vw; ">떠나요</h3>
            <!-- 나중에 이모티콘으로 교체 버튼 임시 -->
            <img src="../assets/friend.png" style="margin-left: 8px;width:2%; height:1.2vw;" >
            <span class="imo"> 동행 모집</span>
            <img src="../assets/help2.png" style="margin-left: 8px; width:2%; height:1.2vw;">
            <span class="imo"> 도움 요청</span>
            <button class="plusbtn">더보기</button>
            <div>
                <button class="mainspotbtn">전체</button>
                <button class="mainspotbtn">서울</button>
                <button class="mainspotbtn">경기도</button>
                <button class="mainspotbtn">강원도</button>
                <button class="mainspotbtn">충청남도</button>
                <button class="mainspotbtn">충청북도</button>
                <button class="mainspotbtn">전라북도</button>
                <button class="mainspotbtn">전라남도</button>
                <button class="mainspotbtn">경상북도</button>
                <button class="mainspotbtn">경상남도</button>
                <button class="mainspotbtn">제주도</button>
            </div>
            <div>
              <!-- 6개로 해서 두 줄로 나오게 할 것 -->
              <!-- 지역이어야 함 -->
              <v-col
                cols="12"
                sm="4"
                style="display:inline-block; padding:6px;"
                v-for="togetherSD in togetherSDs" :key="togetherSD.id"
              >
              <ScheduleCard :data="togetherSD.id" :schedule="togetherSD"/>
              </v-col>
            </div>
        </div>
        <div >
        </div>
      </div>
      <div>
        <div class="mb-3 mt-2">
            <h1 style="display:inline; color:#FF9617; font-size:2.7vw;">BEST</h1>
            <h3 style="display:inline; font-size:1.7vw;  ">여행지</h3>
            <!-- <button class="plusbtn">더보기</button> -->
        </div>
        <div v-for="bestma in bestmain" :key="bestma.id" style="display:inline;" >
            <!-- v-for -->
            <button class="besttag" >BEST</button>
            <SpotCard :spot="bestma" />
        </div>
      </div>
  </div>
</template>

<script>
import SpotCard from '@/components/spots/SpotCard';
import ScheduleCard from '@/components/ScheduleCard';
export default {
    components:{SpotCard,ScheduleCard},
    data () {
      return {
        dummy : {
          'address': "제주특별자치도 서귀포시 토평동",
          'area_code': "Q03",
          'category_code' : "A01010100",
          'content_type_pk': 12,
          'id': 1,
          'image': "http://tong.visitkorea.or.kr/cms/resource/99/1632499_image2_1.jpg",
          'lat': 33.3445,
          'lon': 126.536,
          'overview': "옛날 신선들이 하늘에서 내려와 백록을 타고 놀았다해서 백록담이라 불려졌다 한다. 둘레 약 2천여미터, 깊이가 약 100여 미터의 커다란 화산호인 백록담을 한 바퀴 돌고 나면 제주 섬 해안 도로를 다 돌아다닌 것이나 진배없다. 높이 1,950m이다. 남한에서 가장 높은 산이다. 제3기 말∼제4기 초에 분출한 휴화산이다. 현무암으로 이루어져 있으며 줄기는 제주도 중앙에서 동서로 뻗는다. 남쪽은 경사가 심한 반면 북쪽은 완만하고, 동서쪽은 비교적 높으면서도 평탄하다. 정상에는 둘레 약 3㎞, 지름 500m의 화구호인 백록담(白鹿潭)이 있으며, 주위 사방에 흙붉은오름[土赤岳]·사라오름[砂羅岳]·성널오름[城板岳]·어승생오름[御乘生岳] 등 360여 개의 측화산을 거느리고 있다. 둔덕에 올라서면 산의 높이가 느껴지고 마치 하늘에 두둥실 떠 있는 듯한 멋진 환상을 맛보게 된다. 한편 한라산은 천연기념물 제182호인 한라산 천연보호구역으로 지정, 보호되고 있다.",
          'tel': "064-713-9950",
          'tel_name': null,
          'title': "한라산 백록담",
        },
        bestmain:[],
        togetherSDs:[],
      }
    },
    methods: {
      getTogetherSD() {
      this.$http
      .get(process.env.VUE_APP_SERVER_URL +`/schedule?title=`
      +`&member_type=&style_type=`
      +`&together=1&advice=`
      +`&start_date=&end_date=`)
      .then(response => {
      this.togetherSDs = response.data.schedule.slice(0,6)
      // console.log(this.helpschedules)
      })
      .catch(error => {
      console.log(error.response)
      })
    }
    },
    created() {
      this.$http
      .get(process.env.VUE_APP_SERVER_URL +`/spots/get_best_spots/`)
      .then(res => {
        this.bestmain = res.data.best_spots.slice(0,3)
        // console.log(this.bestmain)
      })
      .catch(error => {
				console.log(error.response)
        })
      this.getTogetherSD()
    }

}
</script>

<style>
.maincenter {
    margin-top: 1%;
    width:66.6666666%;
    margin-left:16.6666666%;
}
.plusbtn {
    float:right;
    margin-top:18px;
    width:6%;
    font-size:1vw;
    height:2vw;
    border-radius:20px;
    background-color: #FF5E5E;
    color:white;
    outline:none;
    font-family: 'SCDream6'
}
.mainspotbtn {
    margin-right:6px;
    font-family: 'SCDream6';
    color:#707070;
    font-size:0.9vw;
}
.imo {
    font-family: 'SCDream5';
    font-size:0.9vw;
    color:#707070;
}
.besttag {
    z-index:1; 
    /* background-color:#FF9617;  */
    position:absolute; float:left; 
    transform: rotate(-45deg); 
    margin-left:-2.4%; 
    margin-top:2%; 
    height:3vw; 
    width:13%;
    font-size:2.1vw;
    font-family: 'SCDream6';
    color:white;
    border-left: 3vw solid transparent;
    border-right: 3vw solid transparent;
    border-bottom: 3vw solid #FF9617;
    outline: none;
}
</style>