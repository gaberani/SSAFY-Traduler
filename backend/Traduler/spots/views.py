from django.shortcuts import render, get_object_or_404
from django.db.models import Avg


from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Spot, Category, Area, SpotComment, UserSpotFavorite, CustomSpot
from .serializers import SpotSerializer, CategorySerializer, AreaSerializer, SpotCommentSerializer,CustomSpotSerializer, SemiSpotSerializer
from traduler.mixin import *
from traduler.permissions import *

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

    permission_classes=[SpotPermission]

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

        page, result = pageProcess(filtered_spots, self.serializer_class, cur_page, 9, request.user)

        return Response({"page": page, "result": result}, status=status.HTTP_200_OK)

    @action(detail=False)
    def semi_list(self,request):
        serialized_spots = SemiSpotSerializer(self.queryset, many=True)
        return Response(serialized_spots.data)

    def retrieve(self, request, pk):
        spot = self.queryset.get(id=pk)
        serialized_spot = self.serializer_class(spot, context={'user': request.user})
        cur_page = request.GET.get("curPage", 1)

        # 댓글 가져오기
        filtered_comments = self.comment_queryset.filter(spot_pk=pk).order_by('-id')
        page, result = pageProcess(filtered_comments, SpotCommentSerializer, cur_page, 10)


        return Response({
            "spot": serialized_spot.data, 
            "page": page, 
            "comments": result}, 
            status=status.HTTP_200_OK)

    # 가장 평점 높은 스팟 리턴하기 
    @action(detail=False, methods=['GET'])
    def get_best_spots(self, request):
        best_spots_pk = self.comment_queryset.values('spot_pk').annotate(score_avg=Avg('score')).order_by('-score_avg')[:5]
        best_spots = []
        for score_obj in best_spots_pk:
            item = self.queryset.get(id=score_obj['spot_pk'])
            best_spots.append(item)
        serialized_best_spots = self.serializer_class(data=best_spots, context={'user': request.user}, many=True)
        serialized_best_spots.is_valid()
        return Response(serialized_best_spots.data, status=status.HTTP_200_OK)

    # 추천 스팟 리턴
    @action(detail=False, methods=["GET"])
    def get_recommend_spots(self, request):
        random_area = Area.objects.filter(content_type=0).order_by('?')[0]
        recom_spots = self.queryset.filter(area_code__area_code__startswith=random_area.area_code).order_by('?')[:5]
        serialized_recom_spots = self.serializer_class(data=recom_spots, context={'user': request.user}, many=True)
        serialized_recom_spots.is_valid()
        return Response({'recom_area': random_area.area_code_name, 'recom_spots': serialized_recom_spots.data}, status=status.HTTP_200_OK)



    
    @action(detail=True, methods=['POST','DELETE'], permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        spot = self.queryset.get(id=pk)
        user = request.user
        if request.method == "POST":
            if UserSpotFavorite.objects.filter(user_pk=user, spot_pk=spot).exists():
                return Response(status=status.HTTP_202_ACCEPTED)
            UserSpotFavorite.objects.create(user_pk=user, spot_pk=spot)
            return Response(status=status.HTTP_201_CREATED)
        else:
            unlike = get_object_or_404(UserSpotFavorite, user_pk=user, spot_pk=spot)
            unlike.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            



class CustomSpotViewSet(viewsets.ModelViewSet):
    queryset = CustomSpot.objects.all()
    serializer_class = CustomSpotSerializer

    permission_classes=[BasicCRUDPermisson]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_pk=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class SpotCommentViewSet(viewsets.ModelViewSet):
    queryset = SpotComment.objects.all().order_by('-id')
    serializer_class = SpotCommentSerializer

    permission_classes=[BasicCRUDPermisson]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_pk=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)














