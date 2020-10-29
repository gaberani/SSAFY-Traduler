from rest_framework import serializers

from .models import Spot, Category, Area, SpotComment, CustomSpot
from accounts.serializers import UserSerializer


class SpotSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Spot
        fields = "__all__"

    def get_is_liked(self, obj):
        # 현재 유저가 로그인한 사용자인 경우입니당
        if self.context.get('user', False) and self.context['user'].is_authenticated:
            temp_val = obj.liked.all().filter(user_pk=self.context['user']).exists()
        # 로그인 안 한 사용자는 모두 False로 리턴합니다.
        else:
            temp_val = False

        return temp_val


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