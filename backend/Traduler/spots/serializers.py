from rest_framework import serializers
from django.db.models import Avg

from .models import Spot, Category, Area, SpotComment, CustomSpot
from accounts.serializers import UserSerializer


class SpotSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()

    class Meta:
        model = Spot
        fields = "__all__"

    def get_is_liked(self, obj):
        # 현재 유저가 로그인한 사용자인 경우입니당
        if self.context.get('user', False) and self.context['user'].is_authenticated:
            like = obj.liked.all().filter(user_pk=self.context['user']).exists()
        # 로그인 안 한 사용자는 모두 False로 리턴합니다.
        else:
            like = False
        return like

    def get_total_likes(self, obj):
        return obj.liked.count()

    def get_avg_score(self, obj):
        avg_val = obj.spot_comments.aggregate(Avg('score')).get('score__avg', 0)
        if avg_val == None:
            return 0
        else:
            return round(avg_val, 2)


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SpotCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_pk', required=False)
    class Meta:
        model = SpotComment
        fields = "__all__"
        read_only_fields = ('reg_time', 'user_pk')

class CustomSpotSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_pk', required=False)
    class Meta:
        model = CustomSpot
        fields = "__all__"
        read_only_fields = ('user_pk',)