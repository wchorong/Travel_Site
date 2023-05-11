from django.urls import path
from .views import Login, Nickname_set
app_name = 'user_set'
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('sign/', Nickname_set.as_view(), name='nickname_set'),
]