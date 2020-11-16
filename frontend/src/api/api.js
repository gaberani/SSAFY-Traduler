export default {
	// GET 메소드는 제외
	URL: {
		SPOT: {
			CATEGORY: '/category/',
			AREA: '/area/',
			SPOTS: '/spots/', // GET, 뒤에 PK값 붙이면 상세보기
      RECOMMEND: '/spots/get_recommend_spots/',
      BEST: '/spots/get_best_spots/',
			LIKE: '/like/',		// POST : 좋아요, DELETE : 취소
			COMMNET: '/comment/',								// POST : 생성, PATCH : 수정, DELETE : 삭제
			CUSTOM_SPOT_CREATE: '/custom_spots/'			// POST : 생성
		},
		SCHEDULE: {
      SCHEDULES: '/schedule/',
			ADVICE: '/advice/',
			MEMO: '/memo/',
		},
		USER: {
			SIGNUP: '/rest-auth/signup/',
			LOGIN: '/rest-auth/login/',
			LOGOUT: '/rest-auth/logout/',
			MYPAGE: '/mypage/',
			EDITORDEL: '/accounts/', // PATCH: 수정, DELETE: 삭제
		},
		COURSE: '/course/'
	}
}
