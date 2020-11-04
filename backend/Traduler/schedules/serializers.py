from rest_framework import serializers

from .models import MemberType, StyleType, Schedule, Course, ScheduleArea, ScheduleAdvice, UserSchedule

from accounts.serializers import UserSerializer

from spots.models import Spot, CustomSpot
from spots.serializers import SpotSerializer, CustomSpotSerializer


class MemberTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberType
        fields = "__all__"


class StyleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleType
        fields = "__all__"

        
class CourseSerializer(serializers.ModelSerializer):
    spot_info = SpotSerializer(source='spot_pk', required=False)
    custom_spot_info = CustomSpotSerializer(source='custom_spot_pk', required=False)
    
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ('user_pk', 'schedule_pk',)


class ScheduleSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_pk', required=False)
    courses = CourseSerializer(source='course_pk', required=False, many=True)
    class Meta:
        model = Schedule
        fields = "__all__"
        read_only_fields = ('user_pk',)


class ScheduleAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleArea
        fields = "__all__"
        read_only_fields = ('schedule_pk',)


class ScheduleAdviceSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_pk', required=False)
    class Meta:
        model = ScheduleAdvice
        fields = "__all__"
        read_only_fields = ('user_pk',)


class UserScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSchedule
        fields = "__all__"
        read_only_fields = ('user_pk', 'schedule_pk',)