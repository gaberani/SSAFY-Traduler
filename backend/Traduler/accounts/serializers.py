
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

import re

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter

from .models import Spot, UserSpotFavorite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'nickname', 'gender', 'age', 'introduce', 'profile_image']


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



# Favorite Spot Serializer
# class UserSpotFavoriteSerializer(serializers.ModelSerializer):
#     spot_detail1 = SpotSerializer(source='spot_pk', read_only=True)
#     spot_detail2 = serializers.SerializerMethodField()

#     def get_spot_detail2(self, user_spots):
#         return SpotSerializer(user_spots.spot_pk)

#     class Meta:
#         model = UserSpotFavorite
#         fields = ['id', 'user_pk', 'spot_detail1', 'spot_detail2']


# drf - register
# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True, write_only=True)
#     password1 = serializers.CharField(required=True, write_only=True)
#     password2 = serializers.CharField(required=True, write_only=True)
#     nickname = serializers.CharField(required=True, write_only=True)
#     gender = serializers.CharField(required=True, write_only=True)
#     age = serializers.IntegerField(required=True, write_only=True)

#     def validate_password1(self, password):
#         return get_adapter().clean_password(password)

#     def validate(self, data):
#         User = get_user_model()
#         if User.objects.filter(username=data['username']).exists():
#             raise serializers.ValidationError(("이미 존재하는 아이디입니다."))
#         return data

#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError(("비밀번호가 일치하지 않습니다."))
#         return data
        
#     def validate(self, data):
#         User = get_user_model()
#         if User.objects.filter(username=data['nickname']).exists():
#             raise serializers.ValidationError(("이미 존재하는 닉네임입니다."))
#         return data

#     def validate(self, data):
#         if data['gender'] not in ['남성', '여성', '기타']:
#             raise serializers.ValidationError(("올바르지 않은 성별입니다."))
#         return data

#     def get_cleaned_data(self):
#         return {
#             'username': self.validated_data.get('username', ''),
#             'password1': self.validated_data.get('password1', ''),
#             'nickname': self.validated_data.get('nickname', ''),
#             'gender': self.validated_data.get('gender', ''),
#             'age': self.validated_data.get('age', '')
#             }
            
#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         adapter.save_user(request, user, self)
#         user.save()
#         return user