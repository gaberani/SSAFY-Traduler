<template>
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