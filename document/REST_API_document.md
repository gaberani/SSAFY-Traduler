# REST API 문서

## 회원 관리

1. 회원 가입 - token 반환

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

2. 로그인 - token 반환

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

4. 회원 정보 조회 (내 정보 조회) - **Authorization**

    ```bash
    GET /accounts/my_info
    ```

    * 즐겨찾기한 여행지 정보 확인

        ```bash
        GET /accounts/favorite_spots
        ```

        ```json
        "params": {
            "curSpotPage": Int
        }
        ```

    * 작성한 스케줄 확인

        ```bash
        GET /accounts/written_schedules
        ```

        ```json
        "params": {
            "curSchedulePage": Int
        }
        ```

5. 회원 정보 수정 - **Authorization**

    ```bash
    PATCH /accounts
    ```

    ```json
    {
        "nickname": String,
        "profile_image": String,
        "introduce": String
    }
    ```

6. 회원 탈퇴 **- Authorization**

    ```bash
    DELETE /accounts
    ```



## 여행지 정보 관련

- 카테고리 목록 불러오기

    ```bash
    GET /category/
    ```

- Area 코드 목록 불러오기

    ```bash
    GET /area/
    ```

1. 여행지 목록 조회

    1. 검색 기능 - 타이틀과 대분류로 검색

        ```bash
        GET /spots
        ```

        ```json
        "params": {
            "title": String,
            "category": String,
            "area": String
        }
        ```

    2. 추천 여행지 (3개)

        ```bash
        GET /spots/get_recommend_spots
        ```

    3. 평점 높은 여행지 (3개)

        ```bash
        GET /spots/get_best_spots
        ```

2. 여행지 상세 정보 조회 

    ```bash
    GET /spots/{spot_pk}
    ```

    1. 여행지 즐겨찾기 추가 - **Authorization**

        ```bash
        POST /spots/{spot_pk}/like/
        ```

    2. 여행지 즐겨찾기 삭제 - **Authorization**

        ```bash
        DELETE /spots/{spot_pk}/like/
        ```

    3. 여행지 평점 및 댓글

        1. 생성 - **Authorization**

            ```bash
            POST /comment/
            ```

            ```json
            "body": {
                "spot_pk": {여행지_pk},
                "score": Int{여행지_평점},
                "content": String{여행지에 대한 코멘트}
            }
            ```

        2. 수정 - **Authorization**

            ```bash
            PATCH /comment/{comment_pk}/
            ```

            ```json
            "body": {
                "spot_pk": {여행지_pk},
                "score": Int,
                "content": String
            }
            ```

        3. 삭제 - **Authorization**

            ```bash
            DELETE /comment/{comment_pk}
            ```

3. 사용자 커스텀 여행지 생성

    ```json
    POST /custom_spots
    ```

    ```json
    "body": {
    	"title": String,
    	"lat": Float,
    	"lon": Float,
    }
    ```



## 스케쥴 관련

1. 스케줄

    1. 스케줄 검색

        ```bash
        GET /schedule
        ```

        ```json
        "params": {
            "title": String, // 여행지 제목 검색 
            "member_type": Int, // 멤버 구성 타입으로 검색
            "style_type": Int, // 여행 스타일로 검색
            "area_code": String, // 여행지에 특정 지역의 여행지가 포함되었는지 검색
            "together": TINYINT, // 0: 모집 안 함, 1: 모집 중
            "advice": TINYINT, // 0: 도움 필요 X, 1: 도움 필요
            "start_date": String, (2020-11-4) // 시작 일자 이후 시작하는 스캐줄 검색
            "end_date": String (2020-11-4) // 종료 일자 이전에 종료되는 스케줄 검색
        }
        ```

    2. 스케줄 CRUD  

        - 상세 정보 조회

            ```bash
            GET /schedule/{schedule_pk}
            ```

        - 스케줄 생성 - **Authorization** ✔

            ```bash
            POST /schedule/
            ```

            ```json
            "body": {
                "*title":String,
                "overview": String,
                "private": TINYINT,
                "advice": TINYINT,
                "together": TINYINT
            }
            ```

        - 수정 - **Authorization**

            ```bash
            PATCH /schedule/{schedule_pk}/
            ```

        - 삭제 - **Authorization**

            ```bash
            DELETE /schedule/{schedule_pk}/
            ```

    - 스케줄 생성 관련 API

        - 목적지 생성

            ```bash
            POST /schedule_area/
            ```

            ```json
            "body": {
            "schedule_pk" : Int,
            "area_code": String, 
            }
            ```

        - 목적지 수정

        ```json
        PATCH /schedule_area/{schedule_area pk}/
        ```

        - 목적지 삭제

        ```json
        DELETE /schedule_area/{schedule_area pk}/
        ```


### 스케줄 스크랩 기능

- 스크랩 - **Authorization**

    ```bash
    POST /schedule/scrap/
    ```

    ```json
    {
        "schedule_pk": Int
    }
    ```

### 스케줄 참가 및 초대 기능

* 스케줄 참가 신청 - **Authorization**

    ```bash
    POST /join/
    ```

    ```json
    "body": {
        "schedule_pk": Int,
        "content": String
    }
    ```

- 스케줄 참가 승인 - **Authorization**

    ```bash
    POST /join/confirm/
    ```

    ```json
    {
        "user_schedule_pk": Int
    }
    ```

- 내 스케쥴에 다른 사람 초대하기 - Auth

    ```bash
    POST /join/invite/
    ```

    ```json
    "body": {
    	"schedule_pk": {스케쥴 번호},
    	"user_pk" : {초대하는 유저 pk} 
    }
    ```

### 스케줄 내의 코스 관련

- 코스 생성

    ```json
     POST /course/
    ```

    ```json
    "body": {
        "start_time": String, // "2020-11-08 04:00:00"
        "end_time" : String, // "2020-11-08 09:00:00"
        "content" : String,
        "budget_food": Int,
        "budget_transport": Int,
        "budget_room": Int,
        "budget_etc": Int,
        "schedule_pk": Int,
        "custom_spot_pk": Int, // or null
        "spot_pk": Int // or null
    }
    ```

- 코스 수정

    ```bash
    PATCH /course/{course_pk}/
    ```

- 코스 삭제

    ```bash
    DELETE /course/{course_pk}/
    ```

* **코스에 대한 메모 관련 API**

    * 조회

        ```bash
        GET /memo
        ```

        ```json
        "params": {
            "course_pk": Int,
            "curPage": Int
        }
        ```

    * 생성

        ```bash
        POST /memo/
        ```

        ```json
        "body": {
            "course_pk": Int,
            "content": String
        }
        ```

    * 수정 - **Authorization**

        ```bash
        PATCH /memo/{memo_pk}/
        ```

        ```json
        "body": {
            "course_pk": Int,
            "content": String
        }
        ```

    * 삭제 - **Authorization**

        ```bash
        DELETE /memo/{memo_pk}/
        ```

### 스케줄 내의 도움 게시판

- 조회

    ```bash
    GET /advice
    ```

    ```json
    "params": {
        "schedule_pk": Int,
        "curPage": Int
    }
    ```

- 생성 - **Authorization**

    ```bash
    POST /advice/
    ```

    ```json
    {
        "schedule_pk": Int,
        "content": String
    }
    ```

- 수정 - **Authorization**

    ```bash
    PATCH /advice/{advice_pk}/
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



## 신청 관련

* 받은 초대 확인

    ```bash
    GET /join/invitation
    ```

    ```json
    "params": {
        "curPage": Int
    }
    ```

* 신청한 스케줄 확인

    ```bash
    GET /join/requests
    ```

    ```json
    "params": {
        "curPage": Int
    }
    ```

* 참여한 스케줄 확인

    ```bash
    GET /join/joined_schedules
    ```

    ```json
    "params": {
        "curPage": Int
    }
    ```

* 받은 신청 확인

    ```bash
    GET /join/recieved_requests
    ```

    ```json
    "params": {
        "curPage": Int
    }
    ```

