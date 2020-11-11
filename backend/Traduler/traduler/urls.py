"""traduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from rest_framework import routers
from accounts.views import AccountViewSet, UserScheduleViewSet
from spots.views import SpotViewSet, CategoryViewSet, AreaViewSet, CustomSpotViewSet, SpotCommentViewSet
from schedules.views import MemberTypeViewSet, StyleTypeViewSet, ScheduleViewSet, CourseMemoViewSet, ScheduleAdviceViewSet, CourseViewSet, ScheduleAreaViewSet

router = routers.DefaultRouter()

# Accounts
router.register('accounts', AccountViewSet)
router.register('join', UserScheduleViewSet)

# Spots
router.register('spots', SpotViewSet)
router.register('category', CategoryViewSet)
router.register('area', AreaViewSet)
router.register('custom_spots', CustomSpotViewSet)
router.register('comment', SpotCommentViewSet)

# Schedules
router.register('member_type', MemberTypeViewSet)
router.register('style_type', StyleTypeViewSet)
router.register('schedule', ScheduleViewSet)
# router.register('join', UserScheduleViewSet)
router.register('memo', CourseMemoViewSet)
router.register('advice', ScheduleAdviceViewSet)
router.register('course', CourseViewSet)
router.register('schedule_area', ScheduleAreaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # rest-auth
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/signup/', include('rest_auth.registration.urls')),
    
    # JWT
    # JWT 토큰 발행
    path('api/token/', obtain_jwt_token),
    # JWT 유효한지 검증
    path('api/token/verify/', verify_jwt_token),
    # JWT 갱신용
    path('api/token/refresh/', refresh_jwt_token),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.conf import settings
from django.urls import re_path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# swagger 정보 설정, 관련 엔드포인트 추가
# swagger 엔드포인트는 DEBUG Mode에서만 노출
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v2',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
    ]


urlpatterns += [
    path('', include(router.urls))
]