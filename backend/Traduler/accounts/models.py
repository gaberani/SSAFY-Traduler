from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    gender = models.CharField(max_length=2)
    age = models.IntegerField(default=0)
    profile_image = models.ImageField(null=True)
    introduce = models.TextField()


# class Area(models.Model):
#     area_code = models.CharField(primary_key=True, max_length=50) # 지역 코드 (pk값) - 변환 필요!!
#     area_code_name = models.CharField(max_length=50) # 지역 이름
#     content_type = models.IntegerField() # 0: 17개 광역시랑 도 / 1: 각각에 대한 시군구

#     class Meta:
#         managed = False
#         db_table = 'area'


# class Category(models.Model):
#     category_code = models.CharField(primary_key=True, max_length=50) # 카테고리 코드 (pk값)
#     category_name = models.CharField(max_length=50) # 카테고리 이름
#     content_type = models.IntegerField() # 0: 대분류 / 1: 중분류 / 2:소분류

#     class Meta:
#         managed = False
#         db_table = 'category'


# class ContentType(models.Model): # 일단 가져는 왔습니다.
#     content_type_name = models.CharField(max_length=50) # 콘텐츠 타입 이름

#     class Meta:
#         managed = False
#         db_table = 'content_type'


# class Spot(models.Model):
#     title = models.CharField(max_length=50) # title ... 이름
#     overview = models.TextField(blank=True, null=True) # 개요
#     lon = models.FloatField() # 위도랑 경도
#     lat = models.FloatField()
#     tel = models.CharField(max_length=50, blank=True, null=True) # 031-000-0000 
#     tel_name = models.CharField(max_length=50, blank=True, null=True) # 관리사무소
#     image = models.TextField() # URL이 들어갈텐데. 길이를 가늠할 수 없어서
#     address = models.CharField(max_length=50, blank=True, null=True) # 주소
#     content_type_pk = models.ForeignKey(ContentType, on_delete=models.SET_NULL, db_column='content_type_pk', blank=True, null=True)
#     area_code = models.ForeignKey(Area, on_delete=models.SET_NULL, db_column='area_code', blank=True, null=True)
#     category_code = models.ForeignKey(Category, on_delete=models.SET_NULL, db_column='category_code', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'spot'


# class UserSpotFavorite(models.Model): # 즐겨찾기
#     user_pk = models.ForeignKey(User, related_name="liked_person", on_delete=models.CASCADE, db_column="user_pk")
#     spot_pk = models.ForeignKey(Spot, related_name="liked_spot", on_delete=models.CASCADE, db_column="spot_pk")

#     class Meta:
#         managed = False
#         db_table = 'user_spot_favorite'

