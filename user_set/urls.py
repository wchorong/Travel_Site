from django.urls import path
from .views import Login, Nickname_set, User_retouch
app_name = 'user_set'
urlpatterns = [
    path('login/', Login.as_view(), name='login'), # 로그인 페이지
    path('sign/', Nickname_set.as_view(), name='nickname_set'), # 회원가입 페이지
    path('user_retouch/', User_retouch.as_view(), name='user_retouch'), # 유저 정보 수정
]