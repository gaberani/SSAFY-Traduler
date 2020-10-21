# 회원 관리

1. 회원 가입 - token 반환해줌!

    ```bash
    POST /rest-auth/signup
    ```

    ```json
    {
        "username": String,
        "password": String,
        "nickname": String,
        "age": Int,
        "gender": String 
    }
    ```

2. 로그인 - token 반환해줌!

    ```bash
    POST /rest-auth/login
    ```

    ```json
    {
        "username": String,
        "password": String
    }
    ```

3. 로그아웃 - **Authorization**

    ```bash
    POST /rest-auth/logout
    ```

4. 회원 정보 조회 (user_pk가 없다면 내 정보 조회, 있다면 해당하는 유저 조회) - **Authorization**

    ```bash
    GET /accounts/{user_pk}
    ```

5. 회원 정보 수정 - **Authorization**

    이미지는 이미지 서버에 올린 후 return 값을 받아서 추가할 것

    ```bash
    PATCH /accounts
    ```

    ```json
    {
        profile_image: String,
        introduce: String
    }
    ```

6. 회원 탈퇴 **- Authorization**

    ```bash
    DELETE /accounts
    ```

# 여행지 정보 관련

1. 여행지 목록 조회

    1. 검색 기능 - 타이틀과 카테고리(대분류, 중분류, 소분류 포함된 "카테고리 코드")로 검색

        ```bash
        GET /spots?title=검색어&category=카테고리코드
        ```

        ```json
        {
            "title": String,
            "category": String,
        }
        ```

    2. 현재 작성 중인 여행코스에 포함된 여행지 - **Authorization**

        ```bash
        GET /spots/writing
        ```

    3. 추천 여행지 (3개)

        ```bash
        GET /spots/recommend
        ```

2. 여행지 상세 정보 조회

    ```bash
    GET /spots/{spot_pk}
    ```

    평균 평점 / 즐겨찾기 수 / 댓글 정보들도 전달 필요

3. 여행지 즐겨찾기 추가 - **Authorization**

    ```bash
    POST /spots/like
    ```

    - Body

    ```json
    {
        "spot_pk": {여행지_pk}
    }
    ```

4. 여행지 즐겨찾기 삭제 - **Authorization**

    ```json
    DELETE /spots/like/{spot_pk}
    ```

5. 여행지 평점 및 댓글

    - 생성 - **Authorization**

        ```bash
        POST /comment
        ```

        - Body

        ```json
        {
            "spot_pk": {여행지_pk},
            "score": Int{여행지_평점},
            "content": String{여행지에 대한 코멘트} 
        }
        ```

    - 수정 - **Authorization**

        ```bash
        PATCH /comment
        ```

        - Body

        ```json
        {
            "comment_pk" : {comment_pk},
            "score": Int,
            "content": String
        }
        ```

    - 삭제 - **Authorization**

        ```bash
        DELETE /comment/{comment_pk}
        ```

# 스케쥴 관련

1. 스케쥴

    1. 스케쥴 목록 불러오기

        1. 필터링 (최신순, 스크랩순, 조회순)

            1. 제목검색
            2. 멤버구성 (혼자, 가족, 커플, 멤버구성)
            3. 스케쥴스타일(액티비티, 힐링, 기타, ❓스타일)
            4. 지역별 (8도)
            5. 동행 모집 여부
            6. 조언 요청 여부
            7. 시작 날짜 / 끝 날짜

            ```bash
            GET /schedule?title&member_type&style_type&area_code&together&advice&start_date&end_date
            ```

            ```json
            {
                "title": String,
                "member_type": Int,
                "style_type": Int,
                "area_code": Int,
                "together": TINYINT,
                "advice": TINYINT,
                "start_date": String,
                "end_date": String
            }
            ```

    2. 스케쥴 CRUD

        - 조회

            - 스케쥴 상세 정보 모두 불러오기

                ```bash
                GET /schedule/{schedule_pk}
                ```

        - 생성 - **Authorization**

            ```bash
            POST /schedule
            ```

            ```json
            {
                "title":String,
                "overview": String,
                "private": TINYINT,
                "advice": TINYINT,
                "together": TINYINT,
                "courses": [{
                    "start_time": String,
                    "end_time": String,
                    "content": String,
                    "budget_food": INT,
                    "budget_transport": INT,
                    "budget_entrance": INT,
                    "budget_room": INT,
                    "budget_etc": INT,
                    "spot_pk": INT,
                    "custom_spot_pk": INT
                },
                {
                    "start_time": ,
                    "end_time": ,
                    "content": ,
                    "budget_food": ,
                    "budget_transport": ,
                    "budget_entrance": ,
                    "budget_room": ,
                    "budget_etc": ,
                    "spot_pk": ,
                    "custom_spot_pk": 
                }, ...]
            }
            ```

        - 수정 - **Authorization**

            ```bash
            PATCH /schedule
            ```

            - Body

            ```json
            {
            	"schedule_pk" : {schedule_pk},
            	...
            }
            ```

        - 삭제 - **Authorization**

            ```bash
            DELETE /schedule/{schedule_pk}
            ```

2. 스케쥴 내 상세 과정 메모 - 참가자

    > 스케쥴 참가자들이 각 코스에 대한 의견을 반영할 수 있는 수단

    - 생성 - **Authorization**

        ```bash
        POST /memo
        ```

        ```json
        {
            "course_pk": Int,
            "content": String
        }
        ```

    - 수정 - **Authorization**

        ```bash
        PATCH /memo
        ```

        ```json
        {
            "course_pk": Int,
            "content": String
        }
        ```

    - 삭제 - **Authorization**

        ```bash
        DELETE /memo/{memo_pk}
        ```

3. 도움 게시판

    > 스케쥴에 대한 도움 댓글을 작성할 수 있는 게시판

    - 생성 - **Authorization**

        ```bash
        POST /advice
        ```

        ```json
        {
            "schedule_pk": Int,
            "content": String
        }
        ```

    - 수정 - **Authorization**

        ```bash
        PATCH /advice
        ```

        ```json
        {
            "schedule_pk": Int,
            "content": String
        }
        ```

    - 삭제 - **Authorization**

        ```bash
        DELETE /advice/{advice_pk}
        ```

4. 스케쥴 스크랩

    > 다른 유저의 스케쥴을 스크랩(복사)할 수 있는 기능

    - 스크랩 - **Authorization**

        ```bash
        POST /schedule/scrape
        ```

        ```json
        {
            "schedule_pk": Int
        }
        ```

5. 스케줄 참가

    > 다른 유저의 스케쥴에 참가자로 참여할 수 있는 기능

    - 신청 - **Authorization**

        ```bash
        POST /schedule/join
        ```

        ```json
        {
            "schedule_pk": Int,
            "content": String
        }
        ```

    - 승인 - **Authorization**

        ```bash
        POST /schedule/confirm
        ```

        ```json
        {
            "schedule_pk": Int,
            "user_pk": Int
        }
        ```

# 이미지 서버

1. 업로드 - 이미지 경로 return

    ```bash
    POST /images/upload
    ```

    ```json
    {
        image: BLOB,
    }
    ```

2. 이미지 경로

    ```bash
    GET /images/{image_URL}
    ```