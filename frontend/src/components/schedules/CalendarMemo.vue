<template>
  <div>
		<span style="font-family: SCDream5;">
			{{memo.user.nickname}}: {{userInfo}}
		</span>
		<span v-if="!memoEditFlag" style="font-family: SCDream4;">
			{{memo.content}}
		</span>
		<v-row v-if="memoEditFlag">
			<v-col cols="10">
				<v-text-field
					v-model="newcontent"
					dense
					required
					hide-details="auto"
				></v-text-field>
			</v-col>
			<v-col cols="2">
				<v-btn icon small v-if="memoEditFlag" @click="onClickmemoSubmitBtn()">
					<v-icon>mdi-check-circle</v-icon>
				</v-btn>			
			</v-col>
		</v-row>
		<!-- v-if="memo.user.id === userInfo.id" -->
		<div>
			<v-btn icon small v-if="!memoEditFlag" @click="onClickmemoEditBtn()" alt="수정">
				<v-icon>mdi-pencil</v-icon>
			</v-btn>
			<v-btn icon small v-if="!memoEditFlag" @click="onClickmemoDelBtn()">
				<v-icon color="red">mdi-close</v-icon>
			</v-btn>
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex' 

export default {
	name:'CalendarMemo',
	data() {
		return {
			memo: this.$attrs.onememo,
			memoEditFlag: false,
			newcontent: this.$attrs.onememo.content,
		}
	},
	methods: {
		onClickmemoEditBtn() {
			this.memoEditFlag = !this.memoEditFlag
		},
		onClickmemoDelBtn() {
			this.$emit('Click-Memo-DelBtn')
		},
		onClickmemoSubmitBtn() {
			this.memoEditFlag = !this.memoEditFlag
			this.$emit('Click-Memo-SubmitBtn')
		}
	},
	computed: {
    ...mapGetters(['userInfo'])
  },
}
</script>

<style>

</style>