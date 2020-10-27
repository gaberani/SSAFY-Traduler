from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response

from .models import Spot, Category
from .serializer import SpotSerializer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()





class SpotViewSet(viewsets.ModelViewSet):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer

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

        spot_serializer = self.serializer_class(filtered_spots, many=True)

        return Response(spot_serializer.data)



