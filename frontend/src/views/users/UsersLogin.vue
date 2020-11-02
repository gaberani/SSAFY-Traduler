<template>
	<v-form v-model="valid">
    <v-container>
			<!-- 뷰페이지 타이틀 -->
			<v-row justify="center">
				<h1 class="login-title">LOGIN</h1>
			</v-row>
			
			<!-- 로그인 폼 -->
      <v-row justify="center">
				<v-col cols="2" md="3"></v-col>
        <v-col
          cols="8"
					md="6"
					class="py-0"
        >
          <v-text-field
            v-model="UserLoginData.username"
						filled
						color="#FF5E5E"
						prepend-inner-icon="mdi-account"
            label="아이디를 입력해주세요"
            required
          ></v-text-field>
        </v-col>
				<v-col cols="2" md="3"></v-col>

				<v-col cols="2" md="3"></v-col>
        <v-col
          cols="8"
					md="6"
					class="py-0"
        >
          <v-text-field
            v-model="UserLoginData.password"
						type="password"
						filled
						color="#FF5E5E"
						prepend-inner-icon="mdi-lock"
            label="비밀번호를 입력해주세요"
            required
          ></v-text-field>
        </v-col>
				<v-col cols="2" md="3"></v-col>
				
				<v-col
					cols="8"
					md="6"
				>
					<v-btn 
						block 
						depressed 
						color="#FF5E5E"
						height="48px"
						class="white--text mb-2 change-title-font"
						@click="SubmitLoginData(UserLoginData)"
					>
						로그인
					</v-btn>
					<v-btn 
						block 
						depressed 
						color="#FF9617"
						height="48px"
						class="white--text change-title-font"
						@click="gotoSignup"
					>
						회원가입
					</v-btn>
				</v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
	name: 'UserLogin',
	data() {
		return {
			valid: false,
			UserLoginData: {
				username: '',
				password: '',
			}
		}
	},
	computed: {
    ...mapGetters(["LoginFlag"])
  },
	methods: {
		...mapActions(["SubmitLoginData"]),
		gotoSignup() {
			this.$router.push({name: 'Signup'})
		}
	}
}
</script>

<style scoped>
.login-title {
	color: #FF5E5E;
	text-align: center;
	margin: 20px auto;
	font-size: 45px;
}

.v-btn {
	font-size: 1.25rem;
}
</style>