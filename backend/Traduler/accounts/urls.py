from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.my_info, name='my_info'),
    path('<int:user_id>/', views.user_info, name='user_info')
]
