
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

import re

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter

# from .models import Spot, UserSpotFavorite
from spots.models import Area, Category, ContentType, Spot, UserSpotFavorite
# from spots.serializers import SpotSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'nickname', 'gender', 'age', 'introduce', 'profile_image']

from spots.serializers import SpotSerializer

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField()
    gender = serializers.CharField()
    age = serializers.IntegerField() 

    def validate(self, data):
        User = get_user_model()
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(("이미 존재하는 아이디입니다."))
        if User.objects.filter(nickname=data['nickname']).exists():
            raise serializers.ValidationError(("이미 존재하는 닉네임입니다."))
        if data['age'] < 0 or data['age'] > 100:
            raise serializers.ValidationError(("나이 이상"))
        return data

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'gender': self.validated_data.get('gender', ''),
            'age': self.validated_data.get('age', '')
        }


class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = '__all__'

class UserSpotFavoriteSerializer(serializers.ModelSerializer):
    spot_detail = SpotSerializer(source='spot_pk', required=False) 
    class Meta:
        model = UserSpotFavorite
        fields = 'all'