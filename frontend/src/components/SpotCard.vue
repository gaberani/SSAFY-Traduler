<template >
    <v-dialog
      v-model="dialog"
      max-width="60%"
    >
    <template v-slot:activator="{ on, attrs }">
        <v-card
            class="spotcard"
            width="31.333333%"
        >
            <v-img
                src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
                height="30%"
                v-bind="attrs"
                v-on="on"
                class="imgbtn"
            >
                <button style="margin-left:84%; margin-top:3%; outline:none;">
                <!-- 아이콘 바꾸기 -->
                    <i class="fas fa-star" style="font-size:1.8vw; color:yellow;"></i>
                </button>
            </v-img>

            <v-card-title class="cardtitle"  >
                <button v-bind="attrs" v-on="on" class="titlebtn">Top western road trips</button>
            </v-card-title>

            <v-card-subtitle class="cardcontent">
            1,000 miles of wonder
            </v-card-subtitle>
        </v-card>
    </template>
    <!-- modal -->
      <v-card style="">
        <div class="modalheader">
            <v-card-title class="modaltitle">여행지 이름</v-card-title>
            <v-btn
                color="blue darken-1"
                text
                @click="dialog = false"
                class="modalclose"
            >
                <i class="fas fa-times" style="font-size:1.5rem; color:#FF5E5E"></i>
            </v-btn>
        </div>
        <v-divider style="background-color:#FF5E5E"></v-divider>
        <div class="modalbody" style="height: 30%;">
            <div class="modalimg" >
                <v-img
                src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
                height="30%"
                >
                </v-img>
            </div>
            <div class="modaldetail">
                <center>
                    <span class="mr-2" style="font-size:1.5vw; display:inline-block; width:26%; border:1px #1793FF solid; border-radius:18px;">4.72</span>
                    <span class="ml-2" style="font-size:1.5vw; display:inline-block; width:26%; border:1px #FF1313 solid; border-radius:18px;">
                        <i class="fas fa-star" style="font-size:1.7vw; color:yellow;"></i>872
                    </span>
                    <h3>3333</h3>
                    <h3>3333</h3>
                    <h3>3333</h3>
                    <h3>3333</h3>
                    <h3>3333</h3>
                </center>
            </div>
        </div>
        <v-divider style="margin-top:-8px;"></v-divider>
        <div class="modalcomment">
            <div>
                <select class="selectrate" >
                    <!-- v-model="" -->
                    <option value="" >5</option>
                    <option value="">4.5</option>
                    <option value="" >4</option>
                    <option value="">3.5</option>
                    <option value="" >3</option>
                    <option value="">2.5</option>
                    <option value="">2.0</option>
                    <option value="">1.5</option>
                    <option value="">1</option>
                    <option value="">0.5</option>
                </select>
                <input class="modalinput" style="width:70%;">
                <button class="commentbtn">작성</button>
            </div>
            <div style="margin-left:20px; margin-top:10px;">
                <!-- v-for 댓글 -->
                <!-- 예시 -->
                <div class="mb-1">
                    <span class="commentbdg">4.5</span>
                    <span >여기 좆노잼이에용,,,</span>
                </div>
                <div class="mb-1">
                    <span class="commentbdg">4.5</span>
                    <span >여기 좆노잼이에용,,,</span>
                </div>
                <div class="mb-1">
                    <span class="commentbdg">4.5</span>
                    <span >여기 좆노잼이에용,,,</span>
                </div>
                <div class="mb-1">
                    <span class="commentbdg">4.5</span>
                    <span >여기 좆노잼이에용,,,</span>
                </div>
            </div>
        </div>
        <v-divider class="mt-3 mb-3"></v-divider>
        <div class="spotschedule">
            <h3 style="margin-left:8px;">이 여행지가 포함된 스케줄</h3>
            <center>
            <button class="detailplus mt-3 mb-3">더보기</button>
            </center>
        </div>
      </v-card>
    </v-dialog>
  
  <!-- </v-card> -->
  
</template>
<script>
export default {
    methods: {
        showModal () {
            console.log("Eeee")
            
        }
    },
    data () {
      return {
        dialogm1: '',
        dialog: false,
      }
    },
}
</script>

<style>
.cardtitle {
    font-size:1.3vw;
}
.cardcontent {
    font-size:1vw;
}
.spotcard {
    display:inline-block;
    margin-left:1%;
    margin-right:1%;
}
.titlebtn {
    outline:none;
}
.titlebtn:hover{background-color:rgb(224, 224, 224);}
.imgbtn:hover{cursor: pointer;}
.modalclose {
    float:right;
    margin-right:-81%;
}
.modaltitle {
    display:inline;
    color:white;
    margin-left:-2%;
}
.modalheader {
    background-color:red;
    width:55%;
}
.modalimg {
    width:55%;
    display:inline-block;
}
.modaldetail {
    width:45%;
    display:inline-block;
}
.modalcomment {
    margin-top:15px;
}
.modalinput {
    border: 2px #FF5E5E solid;
    margin-left:10px;
}
.commentbtn {
    background-color:  #FF5E5E;
    height: 30px;
    width: 50px;
    color:white;
    border-radius: 10px;
    margin-left:10px;
}
.commentbdg {
    display: inline-block;
    text-align:center;
    font-size:1rem;
    background-color:#1793FF;
    color:white;
    height:22px;
    width:35px;
    border-radius:12px;
    margin-right: 12px;
}
.detailplus {
    width:70px;
    height:30px;
    border-radius:20px;
    background-color: #FF5E5E;
    color:white;
    outline:none;
}
.selectrate {
    border:2px #FF5E5E solid;
    appearance: button;
    font-size:1.12rem;
    margin-left:10px;
    width: 50px;
}
</style>