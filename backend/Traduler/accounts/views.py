from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, SpotSerializer
from .models import UserSpotFavorite, Spot


from django.db.models import Prefetch



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

        user_spots = UserSpotFavorite.objects.filter(user_pk=user.id).select_related('spot_pk')
        
        # values 사용해서 각각의 column에 접근하기
        # data = user_spots.values('spot_pk__title', 'spot_pk__lon', 'spot_pk__lat')
        # data = user_spots.only('spot_pk')

        # serializer 내부에서 접근하기
        # data = UserSpotFavoriteSerializer(user_spots, many=True)

        # 배열에 추가하면서 직렬화하기
        favorite_spots = []
        for user_spot in user_spots:
            favorite_spots.append(SpotSerializer(user_spot.spot_pk).data)

        return Response({'user': user_serializer.data, 'favorite_spots': favorite_spots})

