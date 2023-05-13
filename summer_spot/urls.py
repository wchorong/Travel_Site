from django.urls import path
from .views import Main_page, Post_make, Select_post, Review_make, Many_image
app_name = 'summer_spot'
urlpatterns = [
    path('', Main_page.as_view(), name='main_page'),
    path('make/', Post_make.as_view(), name='post_make'),
    path('post/<int:pk>/', Select_post.as_view(), name='post'),
    path('post/review/<int:pk>/', Review_make.as_view(), name='review_make'),
    path('post/InputImage/<int:pk>/', Many_image.as_view(), name='many_image'),
]