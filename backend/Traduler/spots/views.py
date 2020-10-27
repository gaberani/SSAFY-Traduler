from django.shortcuts import render
from django.db.models import Avg

from rest_framework import viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response

from .models import Spot, Category, Area, SpotComment
from .serializer import SpotSerializer, CategorySerializer, AreaSerializer, SpotCommentSerializer

# Create your views here.
class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SpotViewSet(viewsets.ModelViewSet):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer
    comment_queryset = SpotComment.objects.all()
    comment_serializer = SpotCommentSerializer

    def list(self, request, *args, **kwargs):
        title = request.GET.get('title', None)
        category_code = request.GET.get('category', None)
        area_code = request.GET.get('area',None)
        filtered_spots = self.queryset
        if title:
            filtered_spots = filtered_spots.filter(title__icontains=title)
        if category_code:
            filtered_spots = filtered_spots.filter(category_code__category_code__startswith=category_code)
        if area_code:
            filtered_spots = filtered_spots.filter(area_code__area_code__startswith=area_code)

        serialized_spots = self.serializer_class(filtered_spots, many=True)

        return Response(serialized_spots.data)

    def retrieve(self, request, pk):
        spot = self.queryset.get(id=pk)
        serialized_spot = self.serializer_class(spot)

        filtered_comments = self.comment_queryset.filter(spot_pk=pk)
        serialized_comments = self.comment_serializer(filtered_comments, many=True)

        average_score = filtered_comments.aggregate(Avg('score'))

        return Response({"spot": serialized_spot.data, "comments":serialized_comments.data, "score": average_score})



