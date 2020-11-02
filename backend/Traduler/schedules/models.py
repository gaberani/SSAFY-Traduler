from django.db import models

from accounts.models import User
from spots.models import Spot, CustomSpot, Area

# Create your models here.

# Schedule 관련 기초 정보 Model
class MemberType(models.Model): # 멤버 구성 방식 / Ex) 혼자, 가족, 친구 등
    member_type_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'member_type'


class StyleType(models.Model): # 여행 스타일 / Ex) 맛집 탐험 / 자연..... 뭐가있을까요
    style_type_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'style_type'


# Schedule Models - 여행 스케줄과 관련된 전체적인 정보 Model
class Schedule(models.Model):
    title = models.CharField(max_length=50)
    overview = models.TextField()
    private = models.IntegerField()   # 공개 여부 / 0: 비공개 / 1: 공개
    advice = models.IntegerField()    # 조언 요청 / 0: 비허용 / 1: 허용
    together = models.IntegerField()  # 동행 모집 / 0: 모집안함 / 1: 모집
    scrap_count = models.IntegerField(default=0) # 스크랩된 횟수 : 0이 기본값
    start_date = models.DateTimeField()          # 전체 일정 시작 날짜
    end_date = models.DateTimeField()            # 전체 일정 종료 날짜
    max_member = models.IntegerField()           # 최대 참여 인원
    member_type_pk = models.ForeignKey(MemberType, on_delete=models.SET_NULL, db_column='member_type_pk', blank=True, null=True)
    style_type_pk = models.ForeignKey(StyleType, on_delete=models.SET_NULL, db_column='style_type_pk', blank=True, null=True)
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_pk')

    class Meta:
        managed = False
        db_table = 'schedule'


# Schdule의 대략적인 목적지를 입력하기. (ex. 1일 ~ 2일: 경상북도 / 3일 ~ 5일: 서울 등)
class ScheduleArea(models.Model):
    schedule_pk = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column='schedule_pk')
    area_code = models.ForeignKey(Area, on_delete=models.SET_NULL, db_column='area_code', blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'schedule_area'


# Schedule에 대한 조언들
class ScheduleAdvice(models.Model):
    content = models.CharField(max_length=100)
    reg_time = models.DateTimeField(auto_now=True)
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_pk')
    schedule_pk = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column='schedule_pk')

    class Meta:
        managed = False
        db_table = 'schedule_advice'


# User와 Schedule 관계 Model (status에 따라서 분기)
class UserSchedule(models.Model):
    status = models.IntegerField(default=0) # 0: 직접 신청한 거 / 1: 초대받은거 / 2: 참여한거...????
    content = models.CharField(max_length=100, blank=True, null=True) # 직접 신청할 경우만 작성..?
    reg_time = models.DateTimeField(auto_now_add=True)
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_pk')
    schedule_pk = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column='schedule_pk')

    class Meta:
        managed = False
        db_table = 'user_schedule'


# Schedule의 세부 일정에 대한 Models
class Course(models.Model):
    start_time = models.DateTimeField()         # 일정 시작 날짜 및 시간
    end_time = models.DateTimeField()           # 일정 종료 날짜 및 시간
    content = models.CharField(max_length=255)  # 일정에 대한 개요
    # 예산의 경우 반정규화 - 식비 / 교통비 / 입장료 / 숙박비 / 기타 로 구성
    budget_food = models.IntegerField(default=0)
    budget_transport = models.IntegerField(default=0)
    budget_entrance = models.IntegerField(default=0)
    budget_room = models.IntegerField(default=0)
    budget_etc = models.IntegerField(default=0)
    schedule_pk = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column='schedule_pk')
    spot_pk = models.ForeignKey(Spot, on_delete=models.SET_NULL, db_column='spot_pk', blank=True, null=True)
    custom_spot_pk = models.ForeignKey(CustomSpot, on_delete=models.SET_NULL, db_column='custom_spot_pk', blank=True, null=True)
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_pk')

    class Meta:
        managed = False
        db_table = 'course'


# 참여자가 작성하는 세부 일정에 대한 코멘트
class CourseMemo(models.Model):
    content = models.CharField(max_length=255)
    reg_time = models.DateTimeField(auto_now=True)
    course_pk = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_pk')
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_pk')

    class Meta:
        managed = False
        db_table = 'course_memo'


