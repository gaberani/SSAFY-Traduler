from rest_framework import serializers

from .models import Spot, Category, Area, SpotComment


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
    class Meta:
        model = SpotComment
        fields = "__all__"
