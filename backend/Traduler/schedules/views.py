from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import MemberType, StyleType, Schedule, Course, ScheduleArea, ScheduleAdvice, UserSchedule, CourseMemo
from .serializers import MemberTypeSerializer, StyleTypeSerializer, ScheduleSerializer, CourseSerializer, ScheduleAreaSerializer, ScheduleAdviceSerializer, UserScheduleSerializer, CourseMemoSerializer
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
    # 스케줄 관련 모델 / Serializer
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    # 코스(스케줄 상세 과정) 관련 모델 / Serializer
    course_queryset = Course.objects.all()
    course_serializer_class = CourseSerializer
    # 스케줄의 목적지 관련 모델 / Serializer
    province_queryset = ScheduleArea.objects.all()
    province_serializer_class = ScheduleAreaSerializer
    # 스케줄 조언 관련 모델 / Serializer
    advice_queryset = ScheduleAdvice.objects.all()
    advice_serializer_class = ScheduleAdviceSerializer
    # 유저-스케줄 참여 이력 관련 모델 / Serializer
    user_schedule_queryset = UserSchedule.objects.all()
    user_schedule_serializer_class = UserScheduleSerializer

    def list(self, request, *args, **kwargs):
        # 각각의 조건이 들어온게 있는지 확인하고, 변수에 할당합니다.
        title = request.GET.get('title', None)
        member_type = request.GET.get('member_type', None)
        style_type = request.GET.get('style_type', None)
        # 지역과 관련된 거는... 어떻게 해야할지 몰라서 놔뒀습니다. (별도 Table로 연결되어있어서 쿼리를 어떻게 구성할지 고민중입니다.)
        # area_code = request.GET.get('area',None)

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
        # if area_code: # 지역 코드 검색...? -> 일단 일치하는거
        #     filtered_schedules = filtered_schedules.filter(area_code = area_code)
        if together:
            filtered_schedules = filtered_schedules.filter(together = together)
        if advice:
            filtered_schedules = filtered_schedules.filter(advice = advice)
        if start_date: # 지정한 시작 일자 이후에 시작하는 스케줄 
            # String 형태로 들어올 때, isoformat()으로 datetime 객체를 만들어야 되는데... 파이썬 3.7부터 제공되는 기능이라서 .... 죄송합니다.
            start_date_split = list(map(int, start_date.split('-')))
            start_time_filter = datetime.datetime(start_date_split[0], start_date_split[1], start_date_split[2], tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
            filtered_schedules = filtered_schedules.filter(start_date__gte = start_time_filter)
        if end_date:   # 지정한 종료 일자 이전에 끝나는 스케줄
            end_date_split = list(map(int, end_date.split('-')))
            end_time_filter = datetime.datetime(end_date_split[0], end_date_split[1], end_date_split[2], tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
            filtered_schedules = filtered_schedules.filter(end_date__lte = end_time_filter)
        
        # 아직 페이지네이션을 고려하지 않고 진행하고 있습니다..
        serialized_schedules = self.serializer_class(filtered_schedules, many=True).data
        # page, result = pageProcess(serialized_course, self.serializer_class, cur_page, 9, request.user)

        # 각각의 스케줄에서 여행지들이 표시된 지도를 보여줄 계획이라고 해서 각 스케줄에 포함된 여행지들의 좌표 데이터를 넣어서 줬습니다.
        for serialized_schedule in serialized_schedules:
            serialized_schedule['coords'] = []
            contained_courses = Course.objects.filter(schedule_pk=serialized_schedule['id'])
            for contained_course in contained_courses:
                # 포함된 코스가 spot / custome_spot 2종류이므로 분기해줬습니다...
                if contained_course.spot_pk:
                    serialized_schedule['coords'].append([contained_course.spot_pk.lat, contained_course.spot_pk.lon])
                else:
                    serialized_schedule['coords'].append([contained_course.custom_spot_pk.lat, contained_course.custom_spot_pk.lon])

        return Response({"schedule": serialized_schedules}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
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

        province_infos = request.data['province_info']
        for province_info in province_infos:
            # 1. 날짜 + 시간으로 형식을 맞춰서 자동으로 datetime 객체를 만드는 방법
            province_info['start_date'] = province_info['start_date'] + ' 00:00'
            province_info['end_date'] = province_info['end_date'] + ' 23:59'

            # 2. 직접 datetime 객체를 만들어서 넣어주는 방법
            # start_date_split = list(map(int, province_info['start_date'].split('-')))
            # start_date_time = datetime.datetime(start_date_split[0], start_date_split[1], start_date_split[2], tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
            # province_info['start_date'] = start_date_time

            # end_date_split = list(map(int, province_info['end_date'].split('-')))
            # end_date_time = datetime.datetime(end_date_split[0], end_date_split[1], end_date_split[2], tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
            # province_info['end_date'] = end_date_time

            serializer_province = self.province_serializer_class(data=province_info)
            serializer_province.is_valid(raise_exception=True)
            serializer_province.save(schedule_pk=schedule)
        
        return Response({'schedule': serializer_schedule.data}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        schedule = self.queryset.get(id=pk)
        serialized_schedule = self.serializer_class(schedule)
        # cur_page = request.GET.get("curPage", 1)

        # 코스 가져오기
        filtered_course = self.course_queryset.filter(schedule_pk=pk)
        serialized_course = self.course_serializer_class(filtered_course, many=True).data

        # 목적지 정보 가져오기
        filtered_province = self.province_queryset.filter(schedule_pk=pk)
        serialized_province = self.province_serializer_class(filtered_province, many=True).data

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
            "province": serialized_province,
            "advice": serialized_advice,
            "is_joined": is_joined}, 
            status=status.HTTP_200_OK)


# UserSchedule View Set
class UserScheduleViewSet(viewsets.ModelViewSet):
    """
        ScheduleViewSet에 너무 많은 기능이 들어가 있다고 생각했습니다.
        게다가 여기에 참가요청한 요청 메시지까지 보여주려면 ... .....
        뭔가 2개의 ViewSet이 하나에 합쳐진 느낌이라서 별도의 ViewSet으로 분리했습니다.
    """
    # 유저-스케줄 참여 이력 관련 모델 / Serializer
    queryset = UserSchedule.objects.all()
    serializer_class = UserScheduleSerializer

    def list(self, request, *args, **kwargs):
        """
            특정 유저에게 초대된 스케줄 목록을 보여줍니다.
            Token이 반드시 필요합니다!!
        """
        # cur_page = request.GET.get('curPage', 1)
        # 해당 유저의 요청 메시지들 중 status가 1인 것들만 가져옵니다.(status==1 : 초대받은 거)
        filtered_user_schedules = self.queryset.filter(user_pk=request.user).filter(status=1)
        # 아직 페이지네이션을 고려하지 않고 진행하고 있습니다..
        serialized_user_schedules = self.serializer_class(filtered_user_schedules, many=True).data
        # page, result = pageProcess(serialized_course, self.serializer_class, cur_page, 9, request.user)

        return Response({"request_message": serialized_user_schedules}, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        schedule_pk = request.data.get('schedule_pk', None)
        schedule = get_object_or_404(Schedule, pk=schedule_pk)
        user = request.user

        # 이미 신청했거나, 참여했거나 아무튼 있는 경우
        if self.queryset.filter(user_pk=user, schedule_pk=schedule).exists():
            return Response({'reason': '이미 참가신청헀거나, 초대받은 스케줄입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        # 그 외의 경우 (저장!)
        else:
            serializer_user_schedule = self.serializer_class(data=request.data)
            serializer_user_schedule.is_valid(raise_exception=True)
            serializer_user_schedule.save(user_pk=user, schedule_pk=schedule)
            return Response({"success": 'success'}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """ 
            특정 스케줄의 참가요청된 요청 메세지들을 보여줍니다.
            pk: 스케줄의 pk
        """
        schedule = get_object_or_404(Schedule, pk=pk)
        # 참가 신청헀지만, 아직 승인되지 않은 신청 메세지들을 보여줍니다.
        filtered_request_messages = self.queryset.filter(schedule_pk=schedule).filter(status=0)
        serialized_request_messages = self.serializer_class(filtered_request_messages, many=True).data
        return Response({"request_messages": serialized_request_messages}, status=status.HTTP_200_OK)

    # 참가 요청 승인입니다.
    @action(detail=False, methods=['POST'])
    def confirm(self, request):
        request_message_pk = request.data.get('user_schedule_pk', None)
        request_message = get_object_or_404(UserSchedule, pk=request_message_pk)

        if request_message.status == 0:
            # 신청한 유저의 경우입니다.
            if request_message.schedule_pk.user_pk == request.user:
                # 요청 메세지에 해당하는 스케줄 작성자가 승인 요청을 보낸 사람과 일치할 경우
                request_message.status = 2
                request_message.save()
                return Response({"success": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"reason": "스케줄 주인이 아닙니다."}, status=status.HTTP_403_FORBIDDEN)
        elif request_message.status == 1:
            # 초대받은 유저의 경우입니다.
            if request_message.user_pk == request.user:
                # 초대받은 사람이, 초대를 승인하는 경우입니다.
                request_message.status = 2
                request_message.save()
                return Response({"success": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"reason": "초대받은 유저가 아닙니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            # 이미 승인된 경우 (status == 2)
            return Response({"reason": "이미 승인된 초대 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)



class CourseMemoViewSet(viewsets.ModelViewSet):
    """
        각 상세 과정에 대한 메모를 작성하고, 수정하고, 삭제하는 ViewSet입니다.
    """
    # Memo / Serializer
    queryset = CourseMemo.objects.all()
    serializer_class = CourseMemoSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        course = get_object_or_404(Course, pk=request.data['course_pk'])
        if UserSchedule.objects.filter(user_pk=user, schedule_pk=course.schedule_pk, status=2).exists():
            # 해당 코스가 포함된 스케줄에 참여한 유저인 경우에만 메모를 작성할 수 있습니다.
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_pk=request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'reason': '스케줄에 참여하지 않은 유저입니다.'}, status=status.HTTP_403_FORBIDDEN)


