## 유저 관련 DB

### User Table

> 유저에 관련된 상세 정보를 저장하는 Table

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
    - 유저 pk 값
- username
    - NOT NULL / Unique / VARCHAR
    - 일반적인 아이디
- password
    - NOT NULL / VARCHAR(암호화)
    - 유저 비밀번호
    - Django 쓰면 자동으로 암호화 해줍니다! (아마도 SHA-256?)
- nickname
    - NOT NULL / Unique / StringVARCHAR
    - 유저 닉네임
- age
    - NOT NULL / INT
    - 유저의 나이
- gender
    - NOT NULL / VARCHAR
    - 유저의 성별 ("남성", "여성", "어느쪽에도 속하지 않음") - 배려 좋음
- profile_image
    - default 값 필요 혹은 NULL / VARCHAR
    - 유저의 프로필 사진 Url(이미지 서버 혹은 그냥 정적파일)
- introduce
    - NULL / VARCHAR
    - 자기소개



## 여행 스케줄 DB

### Schedule Table ㅇ

> 전체 여행 스케줄을 저장하기 위한 Table 입니다.

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
    - 전체 여행 스케줄에 대한 pk 값
- title
    - NOT NULL / VARCHAR
    - 여행 스케줄명
- overview
    - NOT NULL / VARCHAR
    - 여행 스케줄 개요
- private
    - NOT NULL / TINYINT(0: 비공개, 1: 공개)
    - 공개 / 비공개 여부 선택
- advice
    - DEFAULT 0 / NOT NULL / TINYINT(0: 요청X, 1: 요청)
    - 도움요청 여부 선택
- together
    - DEFAULT 0 / NOT NULL / TINYINT(0: 모집X, 1: 모집)
    - 동행 모집 여부 선택
- scrap_count
    - DEFAULT 0 / NOT NULL / INT
    - 스크랩 횟수는 .... 직접 1씩 늘려줘야됩니다!
- member_type_pk
    - NOT NULL / VARCHAR
    - 멤버 구성 방식 저장용 (친구, 가족, 혼자 등)
- style_type_pk
    - NOT NULL / VARCHAR
    - 여행 스타일 (액티비티, 힐링, 역사 탐색 등)
- area_code
    - NOT NULL/INT
    - 전국 8도 + 복수 선택가능
- user_pk
    - User Table FOREIGN KEY
    - 여행 스케줄 작성자

### MemberType Table

> 멤버 구성 방법에 대한 정보

- pk
- member_type_name

### StyleType Table

> 여행 스타일 정보

- pk
- style_type_name

### Course Table

> 각각의 상세 과정을 저장하기 위한 Table입니다.
>
> 메모 관련 내용은 별도 Table로 관리할 계획이라서 빠져있습니다.

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
    - 상세 과정에 대한 pk 값
- start_time
    - NOT NULL / DATETIME
    - 방문 시작 시간(15분 단위)
- end_time
    - NOT NULL / DATETIME
    - 방문 종료 시간(15분 단위)
- content
    - NULL / VARCHAR
    - 여행 호스트가 작성하는 메모입니다.
- 예산 Column들 (5개)
    - 전부 다 NULL / INT / 순서대로 식비, 교통비, 입장료, 숙박비, 기타
    - budget_food
    - budget_transport
    - budget_entrance
    - budget_room
    - budget_etc
- spot_pk
    - NULL / INT
    - Spot Table FOREIGN KEY
    - 여행지와 연결용 Column
- custom_spot_pk
    - NULL / INT
    - Custom_Spot Table FOREIGN KEY
    - DB에 없는, 사용자가 추가한 여행지
- schedule_pk
    - NOT NULL / INT
    - Schedule Table FOREIGN KEY
    - 해당 여행 상세과정이 어떤 여행 코스에 포함된 것인지 저장하는 값

### CourseMemo Table 

> 여행 스케줄 참여자들이 댓글 형식으로 상세 과정에 메모를 입력합니다..

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
    - 댓글의 pk 값
- content
    - NOT NULL / VARCHAR
    - 댓글 내용
- reg_time
    - NOT NULL / DATETIME
- user_pk
    - User Table FOREIGN KEY
- course_pk
    - Course FOREIGN KEY

### ScheduleAdvice Table

> 도움 신청을 한 여행 스케줄에 작성된 댓글 Table

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
    - 댓글의 pk 값
- content
    - NOT NULL / VARCHAR
    - 정보 댓글
- reg_time
    - NOT NULL / DATETIME
    - 등록 시간
- user_pk
    - User Table FOREIGN KEY
    - 작성자
- schedule_pk
    - Schedule Table FOREIGN KEY
    - 여행 스케줄

### ScheduleArea Table 

> 여행 스케줄에 포함된 목적지들

- pk
- course_pk
- area_code_pk



## 여행지 정보 DB

### Spot Table

> 여행지와 관련된 정보를 저장하기 위한 Table 입니다. 데이터는 한국 관광공사의 TOUR API에서 가져옵니다.

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
    - 여행지 정보의 pk 값
- title
    - NOT NULL / VARCHAR
    - 여행지 명칭
- overview
    - NULL / VARCHAR
    - 여행지에 관련된 간단한 설명
- lon
    - NOT NULL / FLOAT
    - 여행지의 경도
- lat
    - NOT NULL / FLOAT
    - 여행지의 위도
- tel
    - NULL / STRING
    - 전화번호
- tel_name
    - NULL / STRING
    - 전화번호 명칭 (관리사무소 등)
- image
    - NOT NULL  / STRING
    - URL 저장 (한국관광공사 URL)
- address
    - NULL / STRING
    - 주소
        - 주소가 없는 경우 → 프론트 처리
- content_type_pk
    - NOT NULL / INT
    - ContentType Table FOREIGN KEY
    - 컨텐츠 타입 테이블과 연결
    - 예) 관광지, 문화시설, 레포츠, 등등
- area_code_pk
    - NOT NULL / INT
    - AreaCode Table FOREIGN KEY
    - 지역코드와 연결용 Column
- category_pk
    - NOT NULL / STRING
    - Category Table FOREIGN KEY
    - 카테고리 테이블 연결용 Column

### ContentType Table

> 여행지에 대한 컨텐츠 정보를 저장하기 위한 테이블입니다.

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
    - 컨텐츠 타입에 대한 pk값
- content_type_name
    - NOT NULL / VARCHAR
    - 컨텐츠 타입 이름
    - 관광지 / 문화시설 / 행사,공연,축제 / 여행코스 / 레포츠 / 숙박 등

### AreaCode Table

> 지역과 관련된 정보 저장용 Table

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
    - 지역 코드 pk값
- area_code_name
    - NOT NULL / VARCHAR
    - 지역 코드명
- type
    - NOT NULL / INT
    - 

### Category Table

> 대분류 + 중분류 + 소분류 B02: 숙박 / B0201: 숙박시설 / B02011600 : 한옥스테이

- category_code
    - NOT NULL / STRING - pk값
    - 카테고리 pk값 (ex. B012333)
- category_name
    - NOT NULL / VARCHAR
    - 코드 내용
- type
    - NOT NULL / INT
    - 코드 타입 (0 : 대분류, 1: 중분류, 2: 소분류)

### SpotComment Table

> 여행지에 대한 평점 및 댓글을 저장하기 위한 Table

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
    - 여행지 댓글 pk값
- content
    - NOT NULL / VARCHAR
    - 여행지에 대한 댓글
- score
    - NOT NULL / INT
    - 여행지에 대한 평점
- reg_time
    - NOT NULL / DATETIME
    - 댓글 등록 시간
- user_pk
    - User Table FOREIGN KEY
    - 작성한 유저
- spot_pk
    - Spot Table FOREIGN KEY
    - 여행지 정보



## 관계 관련 테이블 (M:N)

### UserSchedule Table

> 사용자와 여행 스케줄 참여 여부 Table

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
- user_pk
    - User Table FOREIGN KEY
- schedule_pk
    - Course Table FOREIGN KEY
- reg_time
    - NOT NULL / DATETIME

### UserScheduleRequest Table

> 사용자가 여행 스케줄에 참여 요청 하는 Table

- pk
- user_pk
- schedule_pk
- reg_time
- content

### UserSpotFavorite Table

> 사용자와 여행지 즐겨찾기 정보 Table

- pk
    - NOT NULL / Autoincrement (Unique Key) / INT
- user_pk
    - User Table FOREIGN KEY
- spot_pk
    - Spot Table FOREIGN KEY