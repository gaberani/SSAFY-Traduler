from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import MemberType, StyleType, Schedule, Course, ScheduleArea, ScheduleAdvice, UserSchedule, CourseMemo, ScheduleAdvice
from .serializers import MemberTypeSerializer, StyleTypeSerializer, ScheduleSerializer, CourseSerializer, ScheduleAreaSerializer, ScheduleAdviceSerializer, UserScheduleSerializer, CourseMemoSerializer, ScheduleAdviceSerializer
from traduler.mixin import *
from traduler.permissions import *

from spots.models import Area

import datetime

# Create your views here.

# MemberType ONLY READ
class MemberTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
        멤버 구성 방식에 대한 ViewSet입니다.
    """
    queryset = MemberType.objects.all()
    serializer_class = MemberTypeSerializer


# StyleType ONLY READ
class StyleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
        여행 스타일에 대한 ViewSet입니다.
    """
    queryset = StyleType.objects.all()
    serializer_class = StyleTypeSerializer


# Schedule View Set
class ScheduleViewSet(viewsets.ModelViewSet):
    """
        스케줄 관련 ViewSet입니다.
        포함된, 그리고 현재 굴러는 가는 기능들은 다음과 같습니다.
        list : 스케줄을 조건에 따라 필터링해서 가져올 수 있습니다. / 현재 페이지네이션이 적용되지 않은 상태입니다.
        create : 스케줄을 생성하는 함수입니다.
        retrieve : 스케줄의 상세 정보를 주는 함수입니다.
        scrap : 스크랩 기능을 하는 함수입니다.
        자세한 설명은 각 함수의 아래부분에 주석을 달아두었습니다.
    """
    permission_classes=[BasicCRUDPermisson]
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
        """
            title, member_type, style_type, together, advice, start_date, end_date를 기준으로 필터링합니다.
            area_code는 왜 빠졌나면.... 음...
                1. 스케줄에 포함된 목적지(province)를 검색해서 가져오거나 (별도 Table에 존재)
                2. 대표 목적지를 설정해서 그걸 기준으로 가져오거나 인데......
                뭘 선택해야할지 모르겠어서 기능 구현은 미뤄두었습니다.
            추가적으로 각 스케줄에 포함된 여행지들의 위도, 경도를 2차원 리스트 형태로 가져옵니다.
        """
        # 각각의 조건이 들어온게 있는지 확인하고, 변수에 할당합니다.
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
        filtered_schedules = self.queryset.filter(private=0)

        # 이하 필터링 내용을... 한번에 할 수 있는 방법을 써볼까 고민하고있습니다. / 쿼리문을 String 형태로 짜고 한번에 필터링 한다거나..?
        if title: # 제목 검색 -> 제목에 포함되는거 가져옴
            filtered_schedules = filtered_schedules.filter(title__icontains=title)
        if member_type: # 맴버 구성 방식 검색 -> 일치하는거 가져옴
            filtered_schedules = filtered_schedules.filter(member_type_pk = member_type)
        if style_type: # 여행 스타일 검색 -> 일치하는거 가져옴
            filtered_schedules = filtered_schedules.filter(style_type_pk = style_type)
        if together:
            filtered_schedules = filtered_schedules.filter(together = together)
        if advice:
            filtered_schedules = filtered_schedules.filter(advice = advice)
        if start_date: # 지정한 시작 일자 이후에 시작하는 스케줄
            start_test = datetime.datetime.strptime(start_date+'-+0900', '%Y-%m-%d-%z')
            filtered_schedules = filtered_schedules.filter(start_date__gte = start_test)
        if end_date:   # 지정한 종료 일자 이전에 끝나는 스케줄
            end_test = end_date + ' 23:59+09:00'
            filtered_schedules = filtered_schedules.filter(end_date__lte = end_test)

        empty_queryset = Schedule.objects.none()
        for filtered_schedule in filtered_schedules:
            if filtered_schedule.contained_provinces.all().filter(area_code=area_code).exists():
                empty_queryset |= self.queryset.filter(id=filtered_schedule.id)
        
        # 아직 페이지네이션을 고려하지 않고 진행하고 있습니다..
        serialized_schedules = self.serializer_class(empty_queryset, many=True).data
        # page, result = pageProcess(serialized_course, self.serializer_class, cur_page, 9, request.user)

        # 각각의 스케줄에서 여행지들이 표시된 지도를 보여줄 계획이라고 해서 각 스케줄에 포함된 여행지들의 좌표 데이터를 넣어서 줬습니다.
        # 이미 직렬화된 데이터라서 ... 코스를 역참조로 가져오질 못하네요...... 어쩔수 없이 filter로 찾으면서 좌표를 넣어주었습니다.
        # for filtered_schedule in empty_queryset:
        #     serialized_schedule['coords'] = []
        #     contained_courses = filtered_schedule.contained_courses.all()
        #     sum_lat, sum_lon = 0, 0
        #     for contained_course in contained_courses:
        #         # 포함된 코스가 spot / custome_spot 2종류이므로 분기해줬습니다...
        #         if contained_course.spot_pk:
        #             serialized_schedule['coords'].append([contained_course.spot_pk.lat, contained_course.spot_pk.lon])
        #             sum_lat += contained_course.spot_pk.lat
        #             sum_lon += contained_course.spot_pk.lon
        #         else:
        #             serialized_schedule['coords'].append([contained_course.custom_spot_pk.lat, contained_course.custom_spot_pk.lon])
        #     serialized_schedule['avg_coord'] = [sum_lat/len(serialized_schedule['coords']), sum_lon/len(serialized_schedule['coords'])]
        
        # return Response({"schedule": serialized_schedules}, status=status.HTTP_200_OK)

        for serialized_schedule in serialized_schedules:
            serialized_schedule['coords'] = []
            contained_courses = Course.objects.filter(schedule_pk=serialized_schedule['id'])
            sum_lat, sum_lon = 0, 0
            for contained_course in contained_courses:
                # 포함된 코스가 spot / custome_spot 2종류이므로 분기해줬습니다...
                if contained_course.spot_pk:
                    serialized_schedule['coords'].append([contained_course.spot_pk.lat, contained_course.spot_pk.lon])
                    sum_lat += contained_course.spot_pk.lat
                    sum_lon += contained_course.spot_pk.lon
                else:
                    serialized_schedule['coords'].append([contained_course.custom_spot_pk.lat, contained_course.custom_spot_pk.lon])
            serialized_schedule['avg_coord'] = [sum_lat/len(serialized_schedule['coords']), sum_lon/len(serialized_schedule['coords'])]
        
        return Response({"schedule": serialized_schedules}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
            데이터는 schedule_info / course_info / province_info 로 구분되어 들어옵니다.
            (schedule_info 는 객체, 나머지는 객체의 배열로 들어옵니다.)
            먼저 Schedule을 만들고, 다른 것들을 만들어서 연결해줍니다.
        """
        # 받은 데이터 중 Schedule 관련 데이터를 먼저 가져와서 schedule 인스턴스부터 만들어줍니다!
        # 이후 만들 Course, Province들에 schedule_pk가 필요해서 이렇게 했습니다.
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

        # 목적지 관련 데이터를 가져오고, 반복문을 통해 각각의 목적지를 만들어줍니다.
        province_infos = request.data['province_info']
        for province_info in province_infos:
            # 1. 날짜 + 시간으로 형식을 맞춰서 자동으로 datetime 객체를 만드는 방법
            province_info['start_date'] = province_info['start_date'] + ' 00:00+09:00'
            province_info['end_date'] = province_info['end_date'] + ' 23:59+09:00'

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
        """
            스케줄 상세 정보를 가져오는 함수입니다.
            스케줄 정보 / 코스 정보 / 목적지 정보 / 조언 / 참여 여부를 한번에 가져옵니다.
            참여여부의 경우 -1(미참여) / 0(승인 대기중) / 1(초대 승인 대기중) / 2(참여중) 입니다.
        """
        user = request.user
        schedule = self.queryset.get(id=pk)
        serialized_schedule = self.serializer_class(schedule)
        # cur_page = request.GET.get("curPage", 1)

        # 코스 가져오기
        contained_courses = schedule.contained_courses.all()
        serialized_course = self.course_serializer_class(contained_courses, many=True).data

        # 목적지 정보 가져오기
        contained_provinces = schedule.contained_provinces.all()
        serialized_province = self.province_serializer_class(contained_provinces, many=True).data

        # 조언 가져오기
        contained_advice = schedule.contained_advice.all()
        serialized_advice = self.advice_serializer_class(contained_advice, many=True).data
        # filtered_advice = self.advice_queryset.filter(schedule_pk=pk)
        # serialized_advice = self.advice_serializer_class(filtered_advice, many=True).data

        # 참여 여부 확인하기
        if request.user.is_authenticated and schedule.submitted_schedule_requests.filter(user_pk=user).exists():
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


    @action(detail=False, methods=['POST'])
    def scrap(self, request):
        """
            스케줄을 스크랩해주는 함수입니다.
            schedule_pk만 가져오면 됩니당....
            스케줄 / 포함된 여행지 / 포함된 목적지를 가져오고
            스크랩부터 순서대로 복사 후 연결해줍니다.
        """
        schedule_pk = request.data['schedule_pk']
        schedule = get_object_or_404(Schedule, pk=schedule_pk)

        if schedule.private == 0:
            # 기존 스케줄의 스크랩 수를 +1 해줍니다.
            schedule.scrap_count += 1
            schedule.save()

            # 새로운 스케줄 생성 전 기존 스케줄의 목적지들 / 상세 과정을 변수에 할당합니다.
            contained_courses = schedule.contained_courses.all()
            contained_provinces = schedule.contained_provinces.all() #ScheduleArea.objects.filter(schedule_pk = schedule)

            # 스케줄을 복사 후, 작성자를 요청자로 바꾸고 여러 설정을 비공개로 전환합니다.
            schedule.pk = None
            schedule.private = 1
            schedule.advice = schedule.together = schedule.scrap_count = 0
            schedule.user_pk = request.user
            schedule.save()

            for course in contained_courses:
                # 모든 포함된 코스 (상세 과정) 들을 작성자 및 연결된 스케줄 변경 후 저장해줍시다!
                course.pk = None
                course.user_pk = request.user
                course.schedule_pk = schedule
                course.save()

            for province in contained_provinces:
                # 모든 포함된 목적지들을 연결된 스케줄 변경 후 저장해줍시다!
                province.pk = None
                province.schedule_pk = schedule
                province.save()

            return Response({'success': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'reason': '비공개 스케줄입니다!!!!'}, status=status.HTTP_403_FORBIDDEN)


# Course
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes=[BasicCRUDPermisson]

    def list(self, request, *args, **kwargs):
        return Response({"하는일 없는 놈"}, status=status.HTTP_200_OK)

    # 스케쥴 생성 후 코스 추가할 때
    def create(self, request, *args, **kwargs):
        schedule_pk = request.data['schedule_pk']
        schedule_instance = get_object_or_404(Schedule, id=schedule_pk)
        #코스 생성하는 사람이 스케쥴 작성일 경우만  
        if schedule_instance.user_pk == request.user: 
            new_course = self.serializer_class(data=request.data)
            if new_course.is_valid(raise_exception=True):
                new_course.save(user_pk=request.user, schedule_pk=schedule_instance)
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


# ScheduleArea
class ScheduleAreaViewSet(viewsets.ModelViewSet):
    queryset = ScheduleArea.objects.all()
    serializer_class = ScheduleAreaSerializer
    permission_classes=[BasicCRUDPermisson]

    def create(self, request, *args, **kwargs):
        schedule_pk = request.data['schedule_pk']
        area_code = request.data['area_code']
        schedule_instance = get_object_or_404(Schedule, id=schedule_pk)
        area_instance = get_object_or_404(Area, area_code=area_code)
        if schedule_instance.user_pk == request.user: #스케쥴 작성자와 내가 같다면
            new_area = self.serializer_class(data=request.data)
            if new_area.is_valid(raise_exception=True):
                new_area.save(schedule_pk=schedule_instance, area_code=area_instance)
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # update와 delete는 db에서 작성자를 확인할 수 있는 컬럼이 없습니다.
    # 그래서 우리가 일일이 schdule 작성자와 동일한지 찾아서 진행해줘야 하는 과정이 추가됩니다.
    def partial_update(self, request, pk):
        area_instance = self.queryset.get(id=pk)
        if area_instance.schedule_pk.user_pk == request.user:
            new_area = self.serializer_class(area_instance, data=request.data, partial=True)
            if new_area.is_valid(raise_exception=True):
                new_area.save()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk):
        area_instance = self.queryset.get(id=pk)
        if area_instance.schedule_pk.user_pk == request.user:
            area_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)



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
    permission_classes=[BasicCRUDPermisson]

    def list(self, request, *args, **kwargs):
        """
            특정 유저에게 자기가 초대받은 스케줄 목록을 보여줍니다.
            Token이 반드시 필요합니다!!
        """
        if request.user.is_authenticated:
            user = request.user
            # cur_page = request.GET.get('curPage', 1)
            # 해당 유저의 요청 메시지들 중 status가 1인 것들만 가져옵니다.(status==1 : 초대받은 거)
            invited_schedules = user.submitted_user_requests.filter(status=1)
            # 아직 페이지네이션을 고려하지 않고 진행하고 있습니다..
            serialized_invited_schedules = self.serializer_class(invited_schedules, many=True).data
            # page, result = pageProcess(serialized_course, self.serializer_class, cur_page, 9, request.user)

            # 해당 유처가 "신청한" 이력도 한번에 들고 옵니다!!
            submit_requests = user.submitted_user_requests.filter(status=0)
            serialized_submit_requests = self.serializer_class(submit_requests, many=True).data

            return Response({"invited_schedules": serialized_invited_schedules, "submit_requests": serialized_submit_requests}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    #신청만!!!!!!
    def create(self, request, *args, **kwargs):
        schedule_pk = request.data.get('schedule_pk', None)
        schedule = get_object_or_404(Schedule, pk=schedule_pk)
        user = request.user

        # 이미 신청했거나, 참여했거나 아무튼 있는 경우
        if schedule.submitted_schedule_requests.filter(user_pk=user).exists():
        # if self.queryset.filter(user_pk=user, schedule_pk=schedule).exists():
            return Response({'reason': '이미 참가신청헀거나, 초대받은 스케줄입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        # 그 외의 경우 (저장!)
        else:
            serializer_user_schedule = self.serializer_class(data=request.data)
            serializer_user_schedule.is_valid(raise_exception=True)
            serializer_user_schedule.save(user_pk=user, schedule_pk=schedule)
            return Response({"success": 'success'}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """    
            38 -> 38번 스케줄에 참가요청 메시지를 보여줌
            특정 스케줄의 참가요청된 요청 메세지들을 보여줍니다.
            pk: 스케줄의 pk
            retrieve를 이렇게 사용하는게 옳은가? 라는 생각이 들었는데... 이왕있는거 좋게좋게 쓰기로 다짐했습니다.
        """
        # 스케쥴 주인인지 확인하기 
        schedule = get_object_or_404(Schedule, pk=pk)
        if request.user.is_authenticated:
            if request.user == schedule.user_pk:
                # 참가 신청헀지만, 아직 승인되지 않은 신청 메세지들을 보여줍니다.
                filtered_request_messages = schedule.submitted_schedule_requests.filter(status=0)
                serialized_request_messages = self.serializer_class(filtered_request_messages, many=True).data
                return Response({"request_messages": serialized_request_messages}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def invite(self, request):
        """
            스케줄 작성자가 사람을 초대하는 경우입니다.
            초대 메세지는 비워져서 옵니다.
        """
        schedule = get_object_or_404(Schedule, pk=request.data['schedule_pk'])
        User = get_user_model()
        user = get_object_or_404(User, pk=request.data['user_pk'])
        if request.user.is_authenticated:
            if schedule.user_pk == request.user:
                if schedule.submitted_schedule_requests.filter(user_pk=user).exists():
                    return Response({'reason': '이미 초대된 사람인데요?'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer_user_schedule = self.serializer_class(data=request.data)
                    if serializer_user_schedule.is_valid(raise_exception=True):
                        serializer_user_schedule.save(status=1, user_pk=user, schedule_pk=schedule)
                        return Response({"success": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"reason": "왜... 이상한 사람이 초대해요?"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # 참가 요청 승인입니다.
    @action(detail=False, methods=['POST'])
    def confirm(self, request):
        """
            참가 요청을 승인해주는 함수입니다.
            1. 신청한 경우
            2. 초대받은 경우
            로 분기해서 각각의 조건을 따진 후 승인 처리를 해줍니다.
        """
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
                return Response({"reason": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        elif request_message.status == 1:
            # 초대받은 유저의 경우입니다.
            if request_message.user_pk == request.user:
                # 초대받은 사람이, 초대를 승인하는 경우입니다.
                request_message.status = 2
                request_message.save()
                return Response({"success": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"reason": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
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

    permission_classes = [BasicCRUDPermisson]

    def create(self, request, *args, **kwargs):
        user = request.user
        course = get_object_or_404(Course, pk=request.data['course_pk'])
        if user.submitted_schedule_requests.filter(schedule_pk=course.schedule_pk, status=2).exists():
        # if UserSchedule.objects.filter(user_pk=user, schedule_pk=course.schedule_pk, status=2).exists():
            # 해당 코스가 포함된 스케줄에 참여한 유저인 경우에만 메모를 작성할 수 있습니다.
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_pk=request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'reason': '스케줄에 참여하지 않은 유저입니다.'}, status=status.HTTP_403_FORBIDDEN)


        

class ScheduleAdviceViewSet(viewsets.ModelViewSet):
    """
        각 스케줄 별 도움 게시글을 작성하는 Viewset입니다.
    """
    # ScheduleAdvice / Serializer
    queryset = ScheduleAdvice.objects.all()
    serializer_class = ScheduleAdviceSerializer
    permission_classes = [BasicCRUDPermisson]

    def create(self, request, *args, **kwargs):
        user = request.user
        schedule = get_object_or_404(Schedule, pk=request.data['schedule_pk'])
        if schedule.advice == 1:
            # 해당 코스가 도움을 요천하는 경우에만 도움 게시글을 작성할 수 있습니다.
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_pk=request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'reason': '도움 댓글이 허용되지 않은 스케줄입니다.'}, status=status.HTTP_403_FORBIDDEN)

    


