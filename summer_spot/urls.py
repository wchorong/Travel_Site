from django.urls import path
from .views import Main_page, Post_make, Select_post, Review_make, Many_image, Post_retouch, \
    Post_images_del, Review_del, Post_search, Post_del,Post_list_make, Post_list_retouch,Post_list, \
    Post_list_del, Post_region, Weather, Weather_search
app_name = 'summer_spot'
urlpatterns = [
    path('', Main_page.as_view(), name='main_page'), # 메인 페이지
    path('make/', Post_make.as_view(), name='post_make'), # 피드 만들기
    path('post/<int:pk>/', Select_post.as_view(), name='post'), # 선택한 피드
    path('post/review/<int:pk>/', Review_make.as_view(), name='review_make'), # 댓글 생성
    path('post/InputImage/<int:pk>/', Many_image.as_view(), name='many_image'), # 피드 이미지
    path('post/post_retouch/<int:pk>/', Post_retouch.as_view(), name='post_retouch'), # 피드 수정
    path('post/del_image/<int:pk>/<int:pk2>', Post_images_del.as_view(), name='post_image_del'), # 피드 이미지 삭제
    path('post/del_review/<int:pk>/<int:pk2>', Review_del.as_view(), name='review_del'), # 댓글 삭제
    path('post/post_search/', Post_search.as_view(), name='post_search'), # 피드 검색
    path('post/post_del/<int:pk>/', Post_del.as_view(), name='post_del'), # 피드 삭제
    path('post/post_list/make/<int:pk>/', Post_list_make.as_view(), name='post_list_make'), # 피드 리스트 생성
    path('post/post_list/retouch/<int:pk>/<int:pk2>', Post_list_retouch.as_view(), name='post_list_retouch'), # 피드 리스트 수정
    path('post/post_list/<int:pk>/<int:pk2>', Post_list.as_view(), name='post_list'), # 선택한 피드 리스트
    path('post/post_list_del/<int:pk>/<int:pk2>', Post_list_del.as_view(), name='post_list_del'), # 선택한 피드 리스트 삭제
    path('post/post_search_region/', Post_region.as_view(), name='post_region'), # 피드 지역 검색
    path('post/weather/<int:pk>/', Weather.as_view(), name='weather'),  # 선택한 피드 날씨
    path('weather_search/', Weather_search.as_view(), name='weather_search'),  # 선택한 피드 날씨
]