from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, SpotSerializer, UserSpotFavoriteSerializer
from .models import UserSpotFavorite

# Create your views here.
@api_view(['Get'])
@permission_classes([IsAuthenticated])
def my_info(request):
    user = request.user
    serializer = UserSerializer(user)
    print(user.id)
    # test = UserSpotFavoriteSerializer(user)
    # print(test.data)
    # favorite_spots = UserSpotFavorite.objects.filter(user_pk=user.id).like_spot
    # print("============", favorite_spots)
    # favorite_spots_serializer = SpotSerializer(favorite_spots, many=True)
    # print(favorite_spots_serializer.data)
    return Response({'user': serializer.data})


@api_view(['Get'])
def user_info(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)
