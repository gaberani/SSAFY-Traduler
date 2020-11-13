from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from .serializers import UserSerializer, UserSpotFavoriteSerializer
# from .models import UserSpotFavorite, Spot
from spots.models import UserSpotFavorite, Spot
from spots.serializers import SpotSerializer

from schedules.models import Schedule, ScheduleAdvice, UserSchedule, Course
from schedules.serializers import UserScheduleSerializer, ScheduleSerializer

from django.db.models import Prefetch
from traduler.mixin import *
from traduler.permissions import *


from django.forms.models import model_to_dict
# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def user_info(self, request, pk):
        user = get_object_or_404(self.queryset, id=pk)
        user_serializer = self.serializer_class(user)

        user_spots = UserSpotFavorite.objects.filter(user_pk=user.id).select_related('spot_pk')
        
        favorite_spots = []
        for user_spot in user_spots:
            favorite_spots.append(SpotSerializer(user_spot.spot_pk).data)

        return Response({'user': user_serializer.data, 'favorite_spots': favorite_spots})

    @action(detail=False)
    def my_info(self, request):
        user = request.user
        user_serializer = self.serializer_class(user)

        return Response({'user': user_serializer.data})

    @action(detail=False, methods=['GET'])
    def favorite_spots(self, request):
        user = request.user
        cur_spot_page = request.GET.get('curSpotPage', 1)

        user_spots = user.liked_spots.all()
        spot_page, favorite_spots = pageProcess(user_spots, UserSpotFavoriteSerializer, cur_spot_page, 3, request.user)
        return Response({'favorite_spots': favorite_spots, 'spot_page': spot_page}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['GET'])
    def written_schedules(self, request):
        user = request.user
        cur_schedule_page = request.GET.get('curSchedulePage', 1)

        user_written_schedules = user.written_schedule.all()
        schedule_page, written_schedules = pageProcess(user_written_schedules, ScheduleSerializer, cur_schedule_page, 3, request.user)

        for serialized_schedule in written_schedules:
            serialized_schedule['coords'] = []
            contained_courses = Course.objects.filter(schedule_pk=serialized_schedule['id']).order_by('start_time')
            sum_lat, sum_lon = 0, 0
            for contained_course in contained_courses:
                if contained_course.spot_pk:
                    serialized_schedule['coords'].append([contained_course.spot_pk.lat, contained_course.spot_pk.lon])
                    sum_lat += contained_course.spot_pk.lat
                    sum_lon += contained_course.spot_pk.lon
                else:
                    serialized_schedule['coords'].append([contained_course.custom_spot_pk.lat, contained_course.custom_spot_pk.lon])
            serialized_schedule['avg_coord'] = [sum_lat/len(serialized_schedule['coords']), sum_lon/len(serialized_schedule['coords'])]

        return Response({'written_schedules': written_schedules, 'schedule_page': schedule_page} )


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

    @action(detail=False, permission_classes=[IsAuthenticated])
    def invitation(self, request):
        cur_page = request.GET.get('curPage', 1)
        user = request.user
        invited_schedules = user.submitted_user_requests.filter(status=1)
        page, serialized_invited_schedules = pageProcess(invited_schedules, self.serializer_class, cur_page, 3, request.user)
        return Response({'page': page, 'invited_schedules': serialized_invited_schedules}, status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def requests(self, request):
        cur_page = request.GET.get('curPage', 1)
        user = request.user
        submit_requests = user.submitted_user_requests.filter(status=0)
        page, serialized_submit_requests = pageProcess(submit_requests, self.serializer_class, cur_page, 3, request.user)
        return Response({'page': page, 'submit_requests': serialized_submit_requests}, status=status.HTTP_200_OK)


    # 특정 스케쥴에 대해 신청하기
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


