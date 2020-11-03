from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import MemberType, StyleType, Schedule, Course, ScheduleAdvice, UserSchedule
from .serializers import MemberTypeSerializer, StyleTypeSerializer, ScheduleSerializer, CourseSerializer, ScheduleAdviceSerializer, UserScheduleSerializer
from traduler.mixin import *
from traduler.permissions import *

import datetime

# Create your views here.

# MemberType ONLY READ
class MemberTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MemberType.objects.all()
    serializer_class = MemberTypeSerializer


# StyleType ONLY READ
class StyleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StyleType.objects.all()
    serializer_class = StyleTypeSerializer


# Schedule View Set
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    course_queryset = Course.objects.all()
    course_serializer_class = CourseSerializer
    advice_queryset = ScheduleAdvice.objects.all()
    advice_serializer_class = ScheduleAdviceSerializer
    user_schedule_queryset = UserSchedule.objects.all()
    user_schedule_serializer_class = UserScheduleSerializer

    def list(self, request, *args, **kwargs):
        title = request.GET.get('title', None)
        member_type = request.GET.get('member_type', None)
        style_type = request.GET.get('style_type', None)
        area_code = request.GET.get('area',None)
        together = request.GET.get('together',None)
        advice = request.GET.get('advice',None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)

        # cur_page = request.GET.get('curPage', 1)
        
        # 공개인 스케줄만 가져옵니다.
        filtered_schedules = self.queryset.filter(private=1)

        # 이하 필터링 내용을... 한번에 할 수 있는 방법을 써볼까 고민하고있습니다.
        if title: # 제목 검색 -> 제목에 포함되는거 가져옴
            filtered_schedules = filtered_schedules.filter(title__icontains=title)
        if member_type: # 맴버 구성 방식 검색 -> 일치하는거 가져옴
            filtered_schedules = filtered_schedules.filter(member_type_pk = member_type)
        if style_type: # 여행 스타일 검색 -> 일치하는거 가져옴
            filtered_schedules = filtered_schedules.filter(style_type_pk = style_type)
        if area_code: # 지역 코드 검색...? -> 일단 일치하는거
            filtered_schedules = filtered_schedules.filter(area_code = area_code)
        if together:
            filtered_schedules = filtered_schedules.filter(together = together)
        if advice:
            filtered_schedules = filtered_schedules.filter(advice = advice)
        if start_date: # 지정한 시작 일자 이후에 시작하는 스케줄 
            start_date_split = list(map(int, start_date.split('-')))
            start_time_filter = datetime.datetime(start_date_split[0], start_date_split[1], start_date_split[2], tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
            filtered_schedules = filtered_schedules.filter(start_date__gte = start_time_filter)
        if end_date:   # 지정한 종료 일자 이전에 끝나는 스케줄
            end_date_split = list(map(int, end_date.split('-')))
            end_time_filter = datetime.datetime(end_date_split[0], end_date_split[1], end_date_split[2], tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
            filtered_schedules = filtered_schedules.filter(end_date__lte = end_time_filter)
        
        serialized_course = self.serializer_class(filtered_schedules, many=True).data
        # page, result = pageProcess(serialized_course, self.serializer_class, cur_page, 9, request.user)

        return Response({"schedule": serialized_course}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
            Data 예시
            {
                "schedule_info": {
                    "title": "테스트",
                    "overview": "테스트222",
                    "private": 0,
                    "advice": 0,
                    "together": 0,
                    "start_date": "2020-11-02 09:00",
                    "end_date": "2020-11-10 18:00",
                    "max_member": 5,
                    "member_type_pk": 1,
                    "style_type_pk": 1
                },
                "course_info": [
                    {
                        "start_time": "2020-11-02 09:00",
                        "end_time": "2020-11-02 12:00",
                        "content": "test",
                        "budget_food": 200,
                        "spot_pk": 52
                    },
                    {
                        "start_time": "2020-11-02 12:00",
                        "end_time": "2020-11-02 15:00",
                        "content": "test222",
                        "budget_food": 200,
                        "budget_entrance": 1000,
                        "spot_pk": 54
                    }
                ]
            }
        """
        # 받은 데이터 중 Schedule 관련 데이터를 먼저 가져와서 schedule 객체부터 만들어줍니다!
        # 이후 만들 Course들에 schedule_pk가 필요해서 이렇게 했습니다.
        serializer_schedule = self.get_serializer(data=request.data['schedule_info'])
        serializer_schedule.is_valid(raise_exception=True)
        serializer_schedule.save(user_pk=request.user)
        # 지금 schedule은 완성 되었습니다.

        schedule_pk = serializer_schedule.data['id']
        schedule = get_object_or_404(Schedule, pk=schedule_pk)

        # 세부 일정 관련 데이터를 가져오고, 반복문을 돌며 각각의 일정을 만들어줍니다.
        course_infos = request.data['course_info']
        for course_info in course_infos:
            serializer_course = self.course_serializer_class(data=course_info)
            serializer_course.is_valid(raise_exception=True)
            serializer_course.save(user_pk=request.user, schedule_pk=schedule)
        
        return Response({'test': 'test'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        schedule = self.queryset.get(id=pk)
        serialized_schedule = self.serializer_class(schedule)
        # cur_page = request.GET.get("curPage", 1)

        # 코스 가져오기
        filtered_course = self.course_queryset.filter(schedule_pk=pk)
        serialized_course = self.course_serializer_class(filtered_course, many=True).data

        # 조언 가져오기
        filtered_advice = self.advice_queryset.filter(schedule_pk=pk)
        serialized_advice = self.advice_serializer_class(filtered_advice, many=True).data

        # 참여 여부 확인하기
        exist_join_data = self.user_schedule_queryset.filter(user_pk=request.user, schedule_pk=schedule).exists()
        if exist_join_data:
            is_joined = self.user_schedule_queryset.get(user_pk=request.user, schedule_pk=schedule).status
        else:
            is_joined = -1

        return Response({
            "schedule": serialized_schedule.data, 
            "course": serialized_course,
            "advice": serialized_advice,
            "is_joined": is_joined}, 
            status=status.HTTP_200_OK)


    # 참가 요청 보내기
    @action(detail=False, methods=['POST'])
    def join(self, request):
        schedule_pk = request.data.get('schedule_pk', None)
        schedule = get_object_or_404(Schedule, pk=schedule_pk)
        user = request.user

        # 이미 신청했거나, 참여했거나 아무튼 있는 경우
        if self.user_schedule_queryset.filter(user_pk=user, schedule_pk=schedule).exists():
            return Response({'fail': 'fail'}, status=status.HTTP_400_BAD_REQUEST)
        # 그 외의 경우 (저장!)
        else:
            serializer_user_schedule = self.user_schedule_serializer_class(data=request.data)
            serializer_user_schedule.is_valid(raise_exception=True)
            serializer_user_schedule.save(user_pk=user, schedule_pk=schedule)
            return Response({"success": 'success'}, status=status.HTTP_200_OK)