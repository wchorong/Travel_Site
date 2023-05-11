from django.urls import path
from .views import Main_page, Post_make
app_name = 'summer_spot'
urlpatterns = [
    path('', Main_page.as_view(), name='main_page'),
    path('make/', Post_make.as_view(), name='post_make'),
]