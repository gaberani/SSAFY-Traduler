<template>
    <v-row>
      <v-col cols="12">
        <v-form>
          <v-row>
            <v-col cols="6">
              <v-text-field
                :value="userInfo.username"
                label="아이디"
                filled
                disabled
                color="#37cdc2"
              ></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                :value="userInfo.age"
                label="나이"
                filled
                disabled
                color="#37cdc2"
              ></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                :value="userInfo.gender"
                label="성별"
                filled
                disabled
                color="#37cdc2"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-text-field
                :value="userInfo.nickname"
                @input="TypeNickname"
                label="닉네임"
                filled
                color="#37cdc2"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-textarea
                :value="userInfo.introduce"
                @input="TypeIntro"
                filled
                name="유저"
                label="간단한 자기소개"
                color="#37cdc2"
                rows="3"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-form>

        <input
                ref="imageInput"
                type="file"
                name="photo"
                id="image_thumbnail"
                hidden
                @change="changePhoto"
        />
        
        <v-avatar
          style="cursor: pointer; width: 10vw; height: 10vw;"
        >
          <img
            :src="
              !!imagePreview
                ? imagePreview
                : require(`@/assets/images/${userInfo.gender}.png`)
            "
            alt="John"
          >
        </v-avatar>

        <a @click="onClickImage">
          <button pill style="color:white;background-color:rgb(249,99,50);">사진 업로드</button>
        </a>

        <v-btn large style="float: right;" @click="updateUser" color="primary"> 변경사항 저장 </v-btn>
        <v-btn large style="float: right;" @click="deleteUser" color="error"> 회원 탈퇴 </v-btn>
      </v-col>
    </v-row>
</template>

<script>
import axios from 'axios'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: "UserInfoUpdate",
  props: {
    userInfo: {
      type: Object
    }
  },
  data() {
    return {
      imageFile: null,
      imagePreview: null,
      nicknameInput: null,
      introduceInput: null,
    }
  },
  computed: {
    ...mapGetters('accounts', ['config']),
  },
  methods: {
    ...mapActions('accounts', ["SubmitLogout"]),
    TypeNickname(event) {
      this.nicknameInput = event;
    },
    TypeIntro(event) {
      this.introduceInput = event;
    },
    onClickImage(){
      this.$refs.imageInput.click();
    },
    changePhoto() {
      const file = event.target.files[0];
      this.imagePreview = URL.createObjectURL(file);
      this.imageFile = file;
    },
    updateUser() {
      let frm = new FormData();
      
      if (this.nicknameInput) {
        frm.append("nickname", this.nicknameInput);
      }
      if (this.introduceInput) {
        frm.append("introduce", this.introduceInput);
      }
      if (this.imageFile) {
        frm.append("profile_image", this.imageFile);
      }

      axios.patch(process.env.VUE_APP_SERVER_URL + '/accounts/' + this.userInfo.id + '/', frm, {
        headers: {
          Authorization: this.config
        }
      })
      .then(res => {
        let updatedInfo = {
          nickname: res.data.nickname,
          introduce: res.data.introduce,
          profile_image: res.data.profile_image,
        };
        this.$emit('updated', updatedInfo);
      })
      .catch(err => console.log(err.response))
    },
    deleteUser() {
      let response = confirm('진짜로 탈퇴하실 거에요...???')
      if (response) {
        let user_id = this.userInfo.id;
        let headers = {headers: {Authorization: this.config}};

        this.SubmitLogout();

        axios.delete(process.env.VUE_APP_SERVER_URL + '/accounts/' + user_id + '/', headers)
        .then(() => {
          alert('지금까지 이용해주셔서 감사합니다.\n\nTraduler 운영자 드림');
          this.$route.push({name: 'Home'});
        })
        .catch(err => console.log(err.response))
      }
    }
  }
}
</script>

<style>

</style>