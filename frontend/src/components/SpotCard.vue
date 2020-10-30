<template >
    <v-dialog
      v-model="dialog"
      max-width="60%"
    >
    <template v-slot:activator="{ on, attrs }">
        <v-card
            class="spotcard"
            width="31.333333%"
            height="30vh 30vw"
        >
            <v-img
                :src="spot.image"
                v-bind="attrs"
                v-on="on"
                class="imgbtn"
            >
                <button style="margin-left:84%; margin-top:3%; outline:none;">
                <!-- 아이콘 바꾸기 -->
                    <i class="fas fa-star" v-if="spot.is_liked==true" @click.stop="unlikespot" style="font-size:1.8vw; color:yellow;"></i>
                    <i class="fas fa-star" v-else @click.stop="likespot" style="font-size:1.8vw; color:black;"></i>
                </button>
            </v-img>

            <v-card-title class="cardtitle" v-bind="attrs" v-on="on" >
                <p v-bind="attrs" v-on="on" class="titlebtn">{{spot.title}}</p>
            </v-card-title>

            <v-card-subtitle class="cardcontent">
            {{spot.address}}
            </v-card-subtitle>
        </v-card>
    </template>
    <!-- modal -->
      <v-card style="border-radius:15px;">
        <div class="modalheader">
            <v-card-title class="modaltitle">{{spot.title}}</v-card-title>
            <v-btn
                color="blue darken-1"
                text
                @click="dialog = false"
                class="modalclose"
            >
                <i class="fas fa-times" style="font-size:1.5rem; color:white;"></i>
            </v-btn>
        </div>
        <v-divider style="background-color:#FF5E5E;"></v-divider>
        <div class="modalbody" style="height: 22vw;">
            <div class="modalimg" >
                <v-img
                :src="spot.image"
                height="21vw"
                >
                </v-img>
            </div>
            <div class="modaldetail mt-3" style="position:absolute" >
                <center>
                    <div>
                        <span v-if="detailspot.score==null" class="mr-2" style="font-size:1.5vw; display:inline-block; width:26%; border:2px #1793FF solid; border-radius:18px; font-family: 'SCDream5';">
                            0</span>
                        <span v-else class="mr-2" style="font-size:1.5vw; display:inline-block; width:26%; border:2px #1793FF solid; border-radius:18px; font-family: 'SCDream5';">
                            {{detailspot.score}}</span>
                        <!--------------- 즐겨찾기 ----------------------------------->
                        <span v-if="spot.is_liked==true" class="ml-2" style="font-size:1.5vw; display:inline-block; width:26%; border:2px #FF1313 solid; border-radius:18px; font-family: 'SCDream5';">
                            <i class="fas fa-star" @click.prevent="unlikespot" style="font-size:1.7vw; color:yellow; "></i>{{detailspot.total_likes}}   
                        </span>
                        <span v-else class="ml-2" style="font-size:1.5vw; display:inline-block; width:26%; border:2px #FF1313 solid; border-radius:18px; font-family: 'SCDream5';">
                            <i class="fas fa-star" @click.prevent="likespot" style="font-size:1.7vw; color:gray; "></i>{{detailspot.total_likes}}    
                        </span>
                    </div>
                </center>
                    <div class="mt-2">
                        <center>
                            <h2 style="font-size:1.5vw">{{spot.title}}</h2>
                            <p style="font-size:1.1vw; margin-bottom:2px;font-family: 'SCDream6'">{{spot.address}}</p>
                            <p style="font-size:1.1vw; margin-bottom:2px;font-family: 'SCDream6'">{{spot.tel}}</p>
                        </center>
                        <p v-html="spot.overview" style="font-size:1vw; font-family: 'SCDream4'; margin-top:5px; margin-left:10px;"></p>
                    </div>
                
            </div>
        </div>
        <v-divider style="margin-top:-1vw;"></v-divider>
        <div class="modalcomment">
            <div>
                <select class="selectrate" v-model="score" >
                    <!-- v-model="" -->
                    <option value="5" >5</option>
                    <option value="4" >4</option>
                    <option value="3" >3</option>
                    <option value="2">2</option>
                    <option value="1">1</option>
                </select>
                <input class="modalinput" style="width:70%;" v-model="content" placeholder="댓글을 입력해주세요.">
                <button @click="writecomment" class="commentbtn">작성</button>
            </div>
            <div style="margin-left:17px; margin-top:10px;">
                <!-- v-for 댓글 폰트크기 비율에 맞춰서 조정해야함-->
                <!-- 예시 -->
                <div class="mb-1" v-for="(comment,index) in spotcomments" :key="index">
                    
                    <span class="commentbdg">{{comment.score}}</span>
                    <span style="font-family: 'SCDream4'" >{{comment.content}}</span>
                    <span style="font-family: 'SCDream6'; float:right; margin-right:18%;">{{comment.user.nickname}}</span>
                    <!-- 삭제 본인만 할 수 있게 해야함 -->
                    <button @click="deleteComment(comment.id,index)" style="margin-left:2%;" ><i class="far fa-times-circle" style="color:red;"></i></button>
                </div>
                <div class="text-center">
                    <!-- 버튼 크기 수정해야댐 -->
                    <v-pagination
                    v-model="page"
                    :length="detailpage.endPage"
                    :total-visible="3"
                    circle
                    ></v-pagination>
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
import axios from 'axios'
import { mapGetters } from "vuex";
export default {
    methods: {
        likespot() {
            let likeStatus = new FormData()
                likeStatus.append('spot_pk',this.spot.id)
            axios.post(`http://127.0.0.1:8000/spots/${this.spot.id}/like/`,likeStatus,{
                headers: {
                    Authorization: this.config,
                },
            })
            .then(({data}) => {
                console.log(data)
                this.spot.is_liked = true
                this.detailspot.total_likes += 1
            }).catch(err => {
                console.log(err.response)
            })
        },
        unlikespot() {
            axios.delete(`http://127.0.0.1:8000/spots/${this.spot.id}/like/`,{
                headers: {
                    Authorization: this.config,
                },
            })
            .then(({data}) => {
                console.log(data)
                this.spot.is_liked = false
                this.detailspot.total_likes -= 1
                
            }).catch(err => {
                console.log(err.response)
            })
        },
        writecomment() {
            let newComment = new FormData()
                newComment.append('spot_pk', this.spot.id)
                newComment.append('score', this.score)
                newComment.append('content', this.content)
            axios.post('http://127.0.0.1:8000/comment/', newComment,{
                headers: {
                    Authorization: this.config,
                },
            })
            .then(({data}) => {
                // console.log(data)
                this.spotcomments.unshift(data)
                this.content=''
            }).catch(err => {
                console.log(err.response)
            })
        },
        deleteComment(commentid,index) {
            axios.delete(`http://127.0.0.1:8000/comment/${commentid}`,{
                headers: {
                    Authorization: this.config,
                },
            })
            .then(({data}) => {
                console.log(data)
                // console.log(index)
                this.spotcomments.splice(index,1)
            }).catch(err => {
                console.log(err.response)
            })
        }
    },
    computed: {
        ...mapGetters(["config"])
    },
    watch: {
        page() {
            axios.get(`http://127.0.0.1:8000/spots/${this.spot.id}?curPage=`+this.page)
				.then(response => {
                this.spotcomments = response.data.comments
				})
				.catch(error => {
				console.log(error)
				})
        }
    },
    props: {
        spot: {
            type:Object,
        },
    },
    data () {
      return {
        dialogm1: '',
        dialog: false,
        detailspot: [],
        spotcomments: [],
        score:'5',
        content:"",
        page:1,
        detailpage: [],
      }
    },
    created () {
            axios.get(`http://127.0.0.1:8000/spots/${this.spot.id}`)
				.then(response => {
				this.detailspot = response.data
                this.spotcomments = this.detailspot.comments
                // console.log(response)
                this.detailpage = this.detailspot.page
                // console.log(this.detailpage)
				})
				.catch(error => {
				console.log(error)
				})
    },
    
}
</script>

<style scoped>
.cardtitle {
    font-size:1vw;
    margin-top:0.5%;
    margin-left:2%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    padding:0;
    display:inline-block;
    font-family: 'SCDream7'
}
.v-application p {
    margin-bottom: 3px;
}
.cardcontent {
    margin-left:2%;
    font-size:0.8vh;
    overflow: hidden;
    text-overflow: ellipsis;
    padding:0;
    white-space: nowrap;
    font-family: 'SCDream4'
}
.spotcard {
    display:inline-block;
    margin-left:1%;
    margin-right:1%;
    margin-bottom:2%;
}
.titlebtn {
    outline:none;
}
.titlebtn:hover{background-color:rgb(224, 224, 224);}
.imgbtn {
    max-width:100%;
    /* max-height:; */
     /* max-height:75%; */
    height:30vh;
}
.imgbtn:hover{cursor: pointer; }
.modalclose {
    float:right;
}
.modaltitle {
    display:inline;
    color:white;
    font-family: 'SCDream5';
    font-size:1.2vw;
}
.modalheader {
    background-color:#FF5E5E;
    width:100%;
}
.modalimg {
    width:55%;
    display:inline-block;
}
.modaldetail {
    width:45%;
    display:inline-block;
    height:20vw;
    overflow: auto;
}
.modalcomment {
    margin-top:15px;
}
.modalinput {
    border: 2px #FF5E5E solid;
    margin-left:10px;
    font-family: 'SCDream4';
    border-radius: 15px;
    outline:none;
    padding-left: 12px;
}
.commentbtn {
    background-color:  #FF5E5E;
    height: 30px;
    width: 50px;
    color:white;
    border-radius: 10px;
    margin-left:10px;
    font-family: 'SCDream4'
}
.commentbdg {
    display: inline-block;
    text-align:center;
    font-size:1rem;
    background-color:#1793FF;
    color:white;
    height:22px;
    width:25px;
    border-radius:12px;
    margin-right: 18px;
    font-family: 'SCDream5'
}
.detailplus {
    width:70px;
    height:30px;
    border-radius:20px;
    background-color: #FF5E5E;
    color:white;
    outline:none;
    font-family: 'SCDream6'
}
.selectrate {
    border:2px #FF5E5E solid;
    appearance: button;
    font-size:1rem;
    margin-left:10px;
    width: 35px;
    font-family: 'SCDream4';
    border-radius: 15px;
    outline:none;
}
</style>