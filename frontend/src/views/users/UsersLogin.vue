<template>
	<v-form v-model="valid">
		
    <v-container>
			<v-row justify="center">
				<h1 class="login-title">LOGIN</h1>
			</v-row>
			
      <v-row justify="center">
				<v-col cols="6" md="3"></v-col>
        <v-col
          cols="12"
					md="6"
					class="py-0"
        >
          <v-text-field
            v-model="UserLoginData.username"
            :rules="nameRules"
						filled
						prepend-inner-icon="mdi-account"
            label="아이디를 입력해주세요"
            required
          ></v-text-field>
        </v-col>
				<v-col cols="6" md="3"></v-col>
				<v-col cols="6" md="3"></v-col>
        <v-col
          cols="12"
					md="6"
					class="py-0"
        >
          <v-text-field
            v-model="UserLoginData.password"
						type="password"
						filled
						prepend-inner-icon="mdi-lock"
            label="비밀번호를 입력해주세요"
            required
          ></v-text-field>
        </v-col>
				<v-col cols="6" md="3"></v-col>
				<v-col
					cols="12"
					md="6"
				>
					<v-btn 
						block 
						depressed 
						color="#FF5E5E"
						height="48px"
						class="white--text mb-2 change-title-font"
					>
						로그인
					</v-btn>
					<v-btn 
						block 
						depressed 
						color="#FF9617"
						height="48px"
						class="white--text change-title-font"
					>
						회원가입
					</v-btn>
				</v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
export default {
	name: 'UserLogin',
	data() {
		return {
			UserLoginData: {
				username: '',
				password: '',
				nickname: '',
				age: null,
				gender: '',
			}
		}
	},
	methods: {
		SubmitLoginData() {

		}
	}
}
</script>

<style>
.login-title {
	color: #FF5E5E;
	text-align: center;
	margin: 20px auto;
	font-size: 45px;
}
</style>