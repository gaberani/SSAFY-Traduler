export default {
	// GET 메소드는 제외
	URL: {
		SPOT: {
			CATEGORY: '/category/',
			AREA: '/area/',
			SEARCH: `/spots?title=${검색어}&category=${카테고리코드}&area=${지역코드}/`,
			WRITING: '/spots/writing/',
			RECOMMEND: '/spots/recommend/',
			READ: `/spots/${spot_pk}/`,
			LIKE: `/spots/${spot_pk}/like/`,		// POST
			UNLIKE: `/spots/${spot_pk}/like/`, 	// DELETE
			COMMNET: '/comment/',								// POST
			COMMNET_EDIT: `/comment/${comment_pk}/`,		// PATCH
			COMMNET_DELETE: `/comment/${comment_pk}/`,	// DELETE
			CUSTOM_CREATE: '/custom_spots/'			// POST
		},
		SCHEDULE: {

		},
		USER: {
			SIGNUP: '/rest-auth/signup/',
			LOGIN: '/rest-auth/login/',
			LOGOUT: '/rest-auth/logout/',
			MYPAGE: '/mypage/',
			EDITORDEL: '/accounts/', // PATCH: 수정, DELETE: 삭제
		}
	}
}
