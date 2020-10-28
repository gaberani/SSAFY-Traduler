from django.shortcuts import render
from django.db.models import Avg


from rest_framework import viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Spot, Category, Area, SpotComment, UserSpotFavorite, CustomSpot
from .serializer import SpotSerializer, CategorySerializer, AreaSerializer, SpotCommentSerializer,CustomSpotSerializer
from .mixin import *
# Create your views here.

# area code ONLY READ
class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer



# category code ONLY READ
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SpotViewSet(viewsets.ModelViewSet):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer
    comment_queryset = SpotComment.objects.all()
    comment_serializer = SpotCommentSerializer

    permission_classes=[]

    def list(self, request, *args, **kwargs):
        title = request.GET.get('title', None)
        category_code = request.GET.get('category', None)
        area_code = request.GET.get('area',None)
        cur_page = request.GET.get('curPage', 1)

        filtered_spots = self.queryset
        if title:
            filtered_spots = filtered_spots.filter(title__icontains=title)
        if category_code:
            filtered_spots = filtered_spots.filter(category_code__category_code__startswith=category_code)
        if area_code:
            filtered_spots = filtered_spots.filter(area_code__area_code__startswith=area_code)

        paginated_result = pageProcess(filtered_spots, self.serializer_class, cur_page, 9)

        return Response(paginated_result)

    def retrieve(self, request, pk):
        spot = self.queryset.get(id=pk)
        serialized_spot = self.serializer_class(spot)
        cur_page = request.GET.get("curPage")

        filtered_comments = self.comment_queryset.filter(spot_pk=pk)
        paginated_comments = pageProcess(filtered_comments, SpotCommentSerializer, cur_page, 10)

        average_score = filtered_comments.aggregate(Avg('score'))

        return Response({"spot": serialized_spot.data, "comments":serialized_comments.data, "score": average_score})

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    @action(detail=True, methods=['POST','DELETE'], permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        spot = self.queryset.get(id=pk)
        user = request.user
        if request.method == "POST":
            new_like = UserSpotFavorite.objects.create(user_pk=user, spot_pk=spot)
            return Response('resource created successfully', status=201)
        else:
            unlike = UserSpotFavorite.objects.get(user_pk=user, spot_pk=spot)
            unlike.delete()
            return Response('resource deleted successfully', status=204)



class CustomSpotViewSet(viewsets.ModelViewSet):
    queryset = CustomSpot.objects.all()
    serializer_class = CustomSpotSerializer

    permission_classes=[]


class SpotCommentViewSet(viewsets.ModelViewSet):
    queryset = SpotComment.objects.all()
    serializer_class = SpotCommentSerializer

    permission_classes=[]

    











