<template>
	<v-form v-model="valid">
		
    <v-container>
			<!-- 뷰페이지 타이틀 -->
			<v-row justify="center">
				<h1 class="signup-title">SIGNUP</h1>
			</v-row>

			<v-row justify="center" no-gutters>
        <v-col
          cols="8"
          md="6"
          class="py-0"
        >
          <v-text-field
            v-model="UserSignupData.username"
            filled
            color="#FF9617"
            prepend-inner-icon="mdi-account"
            placeholder="아이디를 입력해주세요"
            required
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row justify="center" no-gutters>
        <v-col
          cols="8"
          md="6"
          class="py-0"
        >
          <v-text-field
            v-model="UserSignupData.nickname"
            filled
            color="#FF9617"
            prepend-inner-icon="mdi-account"
            placeholder="닉네임을 입력해주세요"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      
      <v-row justify="center" no-gutters>
        <v-col
          cols="8"
          md="6"
          class="py-0"
        >
          <v-text-field
            v-model="UserSignupData.password"
            type="password"
            filled
            color="#FF9617"
            prepend-inner-icon="mdi-lock"
            placeholder="비밀번호를 입력해주세요"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      
      <v-row justify="center" no-gutters>
        <v-col
          cols="8"
          md="6"
          class="py-0"
        >
          <v-text-field
            v-model="UserSignupData.passwordcheck"
            type="password"
            filled
            color="#FF9617"
            prepend-inner-icon="mdi-lock"
            placeholder="비밀번호를 다시 입력해주세요"
            required
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row justify="center" no-gutters>
        <v-col
          cols="8"
          md="6"
          class="py-0"
        >
          <v-text-field
            v-model="UserSignupData.age"
            type="number"
            filled
            color="#FF9617"
            placeholder="나이를 입력해주세요"
            required
          >
            <template v-slot:prepend-inner>
              <img width="24" height="24" src="@/assets/age.png" alt="age" class="grayscale">
            </template>
          </v-text-field>
        </v-col>
      </v-row>

      <v-row justify="center" no-gutters>
        <v-col
          cols="8"
          md="6"
          class="py-0"
        >
          <h2>성별을 선택해주세요</h2>
        </v-col>
      </v-row>

      <v-row 
          justify="space-around"
          no-gutters
          class="my-5"
        >
          <v-col cols="3"></v-col>
          <v-col cols="1">
            <v-icon
              v-if="UserSignupData.gender==='여자'"
              @click="onClickWoman"
              x-large
              color="#FF890E"
            >mdi-face-woman</v-icon>
            <v-icon 
              v-else
              @click="onClickWoman"
              x-large
            >mdi-face-woman</v-icon>
          </v-col>

          <v-col cols="1">
            <v-icon
              v-if="UserSignupData.gender==='남자'"
              @click="onClickMan"
              x-large
              color="#FF890E"
            >mdi-face</v-icon>
            <v-icon
              v-else
              @click="onClickMan"  
              x-large
            >mdi-face</v-icon>
          </v-col>
          <v-col cols="3"></v-col>
        </v-row>

      <v-row justify="center" no-gutters>
        <v-col
					cols="8"
					md="6"
				>
					<v-btn 
						block 
						depressed 
						color="#FF9617"
						height="48px"
						class="white--text change-title-font"
						@click="SubmitSignupData(UserSignupData)"
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
  name: 'UserSignup',
	data() {
		return {
      valid: false,
			UserSignupData: {
        username: '',
        nickname: '',
				password: '',
				passwordcheck: '',
        gender: null,
        age: null
			}
		}
	},
	methods: {
		SubmitSignupData() {
      console.log('TRY signup')
    },

    // 성별 입력 메서드
    onClickWoman() {
      if (this.UserSignupData.gender !== '여자') {
        this.UserSignupData.gender='여자'
      }
      else {
        this.UserSignupData.gender = null
      } 
    },
    onClickMan() {
      if (this.UserSignupData.gender !== '남자') {
        this.UserSignupData.gender='남자'
      }
      else {
        this.UserSignupData.gender = null
      }
    },

	}
}
</script>

<style>
.signup-title {
	color: #FF9617;
	text-align:center;
	margin-bottom:10px;
	font-size:45px;
}
.v-btn {
	font-size: 1.25rem;
}
.v-input__slot {
  margin-bottom: 0px;
}

.grayscale { filter: grayscale(100%); }
</style>