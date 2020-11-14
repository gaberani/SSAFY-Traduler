<template>
  <v-row v-if="!isEdit" style="margin-top: 2vw;">
    <v-col cols="2" offset="1">
      <v-rating
        v-model="comment.score"
        color="yellow darken-3"
        empty-icon="$ratingFull"
        readonly
        dense
        style="margin-top: 0.5vw;"
      ></v-rating>
    </v-col>
    
    <v-col cols="5">
      <span style="font-family: 'SCDream4'" >{{comment.content}}</span>
    </v-col>

    <v-col cols="4" class="d-flex" style="flex-direction: column;">
      <div style="margin-right:18%;">
        <v-btn v-if="username == comment.user.username" @click="deleteComment" text color="error" style="float: right;">삭제</v-btn>
        <v-btn v-if="username == comment.user.username" @click="changeMod" text color="primary" style="float: right;">수정</v-btn>
      </div>
      <div style="margin-right:18%;">
        <span style="font-family: 'SCDream6'; float:right;">{{comment.user.nickname}} ({{ dateForm(comment.reg_time) }})</span>
      </div>
    </v-col>
  </v-row>
  <v-row v-else style="margin-top: 2vw;">
    <v-col cols="2" offset="1">
      <v-rating
        v-model="scoreInput"
        color="yellow darken-3"
        empty-icon="$ratingFull"
        dense
        style="margin-top: 0.5vw;"
      ></v-rating>
    </v-col>
    
    <v-col cols="5" style="text-align: right;">
      <textarea v-model="commentInput" style="width: 100%; height: 100%; border: 1px solid black; font-family: 'SCDream4'" maxlength="80"/>
      <span>{{ commentLength }} / 80자</span>
    </v-col>

    <v-col cols="4" class="d-flex" style="flex-direction: column;">
      <div style="margin-right:18%;">
        <v-btn v-if="username == comment.user.username" @click="updateComment" text color="primary" style="float: right;">수정 완료</v-btn>
      </div>
      <div style="margin-right:18%;">
        <span style="font-family: 'SCDream6'; float:right;">{{comment.user.nickname}} ({{ dateForm(comment.reg_time) }})</span>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "SpotComment",
  props: {
    comment: {
      type: Object,
    },
    index: {
      type: Number,
    }
  },
  data() {
    return {
      isEdit: false,
      scoreInput: this.comment.score,
      commentInput: this.comment.content
    }
  },
  computed: {
    ...mapGetters('accounts', ["userInfo"]),
    username() {
      return sessionStorage.getItem("username");
    },
    commentLength() {
      return this.commentInput.length;
    }
  },
  methods: {
    dateForm(date) {
      return date.slice(0, 10) + ' ' + date.slice(11, 19);
    },
    changeMod() {
      this.isEdit = true;
    },
    updateComment() {
      let commentIdx = this.index
      let commentId = this.comment.id;
      let commentInput = {
        'spot_pk': this.comment.spot_pk,
        'score': this.scoreInput,
        'content': this.commentInput
      };
      this.$emit('updateComment', commentIdx, commentId, commentInput);
      this.isEdit = false;
    },
    deleteComment() {
      this.$emit('deleteComment');
    },
  },
}
</script>

<style>

</style>