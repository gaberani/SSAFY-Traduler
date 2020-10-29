from rest_framework import serializers

from .models import Spot, Category, Area, SpotComment, CustomSpot
from accounts.serializers import UserSerializer


class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SpotCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = SpotComment
        fields = "__all__"
        read_only_fields = ('reg_time', 'user_pk')

class CustomSpotSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = CustomSpot
        fields = "__all__"
        read_only_fields = ('user_pk',)