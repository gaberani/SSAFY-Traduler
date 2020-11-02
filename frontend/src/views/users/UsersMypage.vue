<template>
	<v-container>
		<v-row>
			<v-col cols="2" md="3"></v-col>
			<!-- 회원 정보 -->
				<v-row>
					<v-col>
						<h1>내 정보</h1>
						<v-btn
							@click="GetUserInfo"
						>
							내 정보 확인
						</v-btn>
					</v-col>
				</v-row>

				<v-row>
					<!-- 내 스케줄 -->

					<!-- 스크랩한 스케줄 -->

				</v-row>

				<v-row>
					<v-col></v-col>
					<!-- 동행 스케줄 -->

					<!-- 즐겨찾기한 여행지 -->
				</v-row>
			<v-col cols="2" md="3"></v-col>
		</v-row>
	</v-container>
</template>

<script>
import { mapActions } from 'vuex'

export default {
	name: 'UsersMypage',
	data() {
		return {
			valid: false,
		}
	},
	methods: {
		...mapActions(["GetUserInfo"])
	}
}
</script>

<style>

</style>