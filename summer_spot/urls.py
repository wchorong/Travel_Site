from django.urls import path
from .views import Main_page, Post_make, Select_post, Review_make, Many_image, Post_retouch, \
    Post_images_del, Review_del, Post_search, Post_del
app_name = 'summer_spot'
urlpatterns = [
    path('', Main_page.as_view(), name='main_page'), # 메인 페이지
    path('make/', Post_make.as_view(), name='post_make'), # 피드 만들기
    path('post/<int:pk>/', Select_post.as_view(), name='post'),
    path('post/review/<int:pk>/', Review_make.as_view(), name='review_make'),
    path('post/InputImage/<int:pk>/', Many_image.as_view(), name='many_image'),
    path('post/post_retouch/<int:pk>/', Post_retouch.as_view(), name='post_retouch'),
    path('post/del_image/<int:pk>/<int:pk2>', Post_images_del.as_view(), name='post_image_del'),
    path('post/del_review/<int:pk>/<int:pk2>', Review_del.as_view(), name='review_del'),
    path('post/post_search/', Post_search.as_view(), name='post_search'),
    path('post/post_del/<int:pk>/', Post_del.as_view(), name='post_del'),
]