<template>
  <v-form v-model="valid">
		<h2>유저 회원가입</h2>
    <v-container>
      <v-row>
        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
            v-model="UserLoginData.username"
            :rules="nameRules"
            label="아이디를 입력해주세요"
            required
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
            v-model="UserLoginData.password"
						type="password"
            label="비밀번호를 입력해주세요"
            required
          ></v-text-field>
        </v-col>

				<v-col
          cols="12"
          md="4"
        >
          <v-text-field
            v-model="UserLoginData.passwordcheck"
						type="password"
            label="비밀번호를 다시 입력해주세요"
            required
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          md="4"
        >
          <v-text-field
            v-model="email"
            :rules="emailRules"
            label="E-mail"
            required
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
export default {
  name: 'UserSignup',
	data() {
		return {
			UserLoginData: {
				username: '',
				password: '',
				passwordcheck: '',
				nickname: '',
				age: null,
				gender: '',
			}
		}
	},
	methods: {
		
	}
}
</script>

<style>

</style>