from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

# AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

class BasicCRUDPersmisson(BasePermission):
    """
        조회 : 모든 사용자에게 허용 (목록이든, 특정 요소든)
        생성 : 로그인한 사용자만 허용
        수정 : 작성자만 허용
        삭제 : 작성자 / 관리자만 허용
        사용 예시]
            Spot Comment (여행지 평점)
            Schedule (스케줄)
            Schedule Area (스케줄에서 가는 지역) 등
        
        has_object_persmission 은 list에 대해서 호출되지 않습니다.
        또한, POST 요청의 경우에도 호출되지 않습니다.!!!!

        참고 : https://stackoverflow.com/questions/54783424/drf-has-object-permission-not-called
        참고 : https://stackoverflow.com/questions/43064417/whats-the-differences-between-has-object-permission-and-has-permission-in-drfp/43070831

        실제 사용 시에는 self.check_object_permissions(self.request, obj) 형식으로 사용합니다.
    """
    def has_permission(self, request, view):
        # GET 요청(조회)는 모든 유저에게 허용
        if request.method in SAFE_METHODS:
            return True
        # 그 외 methods는 로그인한 사용자들에 대해서 1차적으로 허용 / POST 요청 권한 처리
        else:
            return request.user.is_authenticated                

    # 해당 method는 GET(list 제외), PUT, PATCH, DELETE 요청에 대한 처리
    def has_object_permission(self, request, view, obj):
        # GET 요청의 경우 (특정 항목에 대한 조회) - 모두 허용
        if request.method in SAFE_METHODS:
            return True
        else:
            # PUT / PATCH 요청 (수정) - 작성자만 허용
            if request.method in ['PUT', 'PATCH']:
                if hasattr(obj, 'user_pk'):
                    return obj.user_pk.id == request.user.id
                # 만약 User 모델일 경우 (회원정보 수정)
                elif obj.__class__ == get_user_model():
                    return obj.id == request.user.id
            # DELETE 요청 (삭제) - 작성자와 관리자 허용
            elif request.method == 'DELETE':
                # 관리자일 경우 허용
                if request.user.is_staff == 1:
                    return True
                # 해당 오브젝트의 작성자일 경우 허용(True)
                elif hasattr(obj, 'user_pk'):
                    return obj.user_pk.id == request.user.id
                # 만약 User 모델일 경우 (회원정보 삭제)
                elif obj.__class__ == get_user_model():
                    return obj.id == request.user.id


class SpotPermission(BasePermission):
    """
        여행지 관련 권한을 처리하기 위한 class입니다.
        C, U, D가 Admin에게만 허용
        R은 모든 사용자에게 허용
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user.is_staff == 1:
                return True
            else:
                return False
    