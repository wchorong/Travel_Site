import html
from collections import Counter
from itertools import groupby

from django.db.models import Count, F, Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import Post_Serializer,Post_Categories_Serializer, Review_Serializer, Many_image_Serializer, \
    Post_list_Serializer
from .models import Post
from user_set.models import User
from lion_project import settings
import requests
from datetime import datetime


class Post_make(APIView): # 휴양지 피드 만들기
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post_Serializer()
        return Response(status=status.HTTP_200_OK, template_name='main/post_make.html',
                        data={'post': post})

    def post(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        user = User.objects.get(id=user_check)
        post = Post_Serializer(data=request.data, context={'user': user})
        if post.is_valid():
                post.save()
                return redirect('summer_spot:main_page')
        else:
            va = post.errors
            error = []
            for key, value in va.items():
                A = [key, value[0]]
                error.append(A)
            return Response(status=status.HTTP_200_OK, template_name='main/post_make.html',
                            data={'post': post, "error": error})

class Main_page(APIView): # 피드 리스트
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        main_table_values = User.objects.filter(id=user_check).values('mood', 'personnel', 'leisure', 'rental_item')
        post_table_values = Post.objects.all().values('mood', 'personnel', 'leisure', 'rental_item', 'id')

        if post_table_values:
            first_queryset = main_table_values
            second_queryset = post_table_values

            first_query = first_queryset[0]
            sorted_queries = sorted(second_queryset,
                                    key=lambda x: len(Counter(x.items()) & Counter(first_query.items())),
                                    reverse=True)
            grouped_queries = []
            for key, group in groupby(sorted_queries,
                                      key=lambda x: len(Counter(x.items()) & Counter(first_query.items()))):
                queries = list(group)
                grouped_queries.append(queries)
            posts = []
            for grouped_mapping in grouped_queries:
                filter_condition = Q()
                for fields_mapping in grouped_mapping:
                    q_objects = Q(**fields_mapping)
                    filter_condition |= q_objects
                my_objects = Post.objects.filter(filter_condition)
                posts.append(my_objects.order_by('-user_check'))

            return Response(status=status.HTTP_200_OK, template_name='lion_2/index.html', data={"post": posts})

        else:
            return Response(status=status.HTTP_200_OK, template_name='lion_2/index.html', data={"post": post_table_values})

class Post_region(APIView): # 지역 검색
    renderer_classes = [TemplateHTMLRenderer]
    def post(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        main_table_values = User.objects.filter(id=user_check).values('mood', 'personnel', 'leisure', 'rental_item')
        post_table_values = Post.objects.filter(region=request.data['searchbox']).values('mood', 'personnel', 'leisure', 'rental_item', 'id')

        if post_table_values:
            first_queryset = main_table_values
            second_queryset = post_table_values

            first_query = first_queryset[0]
            sorted_queries = sorted(second_queryset,
                                    key=lambda x: len(Counter(x.items()) & Counter(first_query.items())),
                                    reverse=True)
            grouped_queries = []
            for key, group in groupby(sorted_queries,
                                      key=lambda x: len(Counter(x.items()) & Counter(first_query.items()))):
                queries = list(group)
                grouped_queries.append(queries)
            posts = []
            for grouped_mapping in grouped_queries:
                filter_condition = Q()
                for fields_mapping in grouped_mapping:
                    q_objects = Q(**fields_mapping)
                    filter_condition |= q_objects
                my_objects = Post.objects.filter(filter_condition)
                posts.append(my_objects.order_by('-user_check'))
                return Response(status=status.HTTP_200_OK, template_name='lion_2/index.html', data={"post": posts})

        else:
                return Response(status=status.HTTP_200_OK, template_name='lion_2/index.html', data={"post": post_table_values})
class Post_search(APIView): # 피드 검색
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        return Response(status=status.HTTP_200_OK, template_name='lion_2/keyword.html')

    def post(self, request):
        user_check = request.session.get('user')
        main_table_values = User.objects.filter(id=user_check).values('mood', 'personnel', 'leisure', 'rental_item')
        post_table_values = Post.objects.all().values('mood', 'personnel', 'leisure', 'rental_item', 'id')

        if post_table_values:
            first_queryset = main_table_values
            second_queryset = post_table_values

            first_query = first_queryset[0]
            sorted_queries = sorted(second_queryset,
                                    key=lambda x: len(Counter(x.items()) & Counter(first_query.items())),
                                    reverse=True)
            grouped_queries = []
            for key, group in groupby(sorted_queries,
                                      key=lambda x: len(Counter(x.items()) & Counter(first_query.items()))):
                queries = list(group)
                grouped_queries.append(queries)
            posts = []
            filters = Q()  # 빈 Q 객체 생성

            if 'mood' in request.data:
                filters &= Q(mood__in=request.data.getlist('mood'))

            if 'personnel' in request.data:
                filters &= Q(personnel__in=request.data.getlist('personnel'))

            if 'leisure' in request.data:
                filters &= Q(leisure__in=request.data.getlist('leisure'))

            if 'rental_item' in request.data:
                filters &= Q(rental_item__in=request.data.getlist('rental_item'))


            mood_choices = dict(Post.MOOD)
            personnel_choices = dict(Post.PERSONNEL)
            leisure_choices = dict(Post.LEISURE)
            rental_item_choices = dict(Post.RENTAL_ITEM)
            mood_key = [mood_choices[key] for key in request.data.getlist('mood')]
            personnel_key = [personnel_choices[key] for key in request.data.getlist('personnel')]
            leisure_key = [leisure_choices[key] for key in request.data.getlist('leisure')]
            rental_item_key = [rental_item_choices[key] for key in request.data.getlist('rental_item')]

            for grouped_mapping in grouped_queries:
                filter_condition = Q()
                for fields_mapping in grouped_mapping:
                    q_objects = Q(**fields_mapping)
                    filter_condition |= q_objects
                my_objects = Post.objects.filter(filter_condition)
                posts.append(my_objects.order_by('-user_check').filter(filters))


            return Response(status=status.HTTP_200_OK, template_name='main/main_page.html', data={"post": posts,
                                                                                                  "mood_key": mood_key,
                                                                                                  'personnel_key': personnel_key,
                                                                                                  'leisure_key': leisure_key,
                                                                                                  'rental_item_key': rental_item_key})

        else:
            return Response(status=status.HTTP_200_OK, template_name='main/main_page.html',
                            data={"post": post_table_values})


class Select_post(APIView): # 선택한 피드
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        check_user = request.session.get('user')
        if check_user is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        post.user_check += 1
        post.save()
        review_set = Review_Serializer(data=request.data)
        count = []
        for i in range(len(post.post_image.all())):
            count.append(i+1)
        return Response(status=status.HTTP_200_OK, template_name='lion_2/detail.html', data={"post": post, 'pk': pk,
                                                                                         'review': review_set,
                                                                                         'check_user': check_user,
                                                                                             "count": count})

class Weather(APIView): # 날씨
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        check_user = request.session.get('user')
        if check_user is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        API_key = settings.WEATHER_API_KEY
        region = post.place_address.split()
        region = f'{region[0]} {region[1]}'
        lat, lon = post.place_y, post.place_x
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_key}'
        response = requests.get(url)
        weather_set = response.json()
        weather, temp, cloud = weather_set['weather'][0]['main'], int(weather_set['main']['temp']), weather_set['clouds']['all']
        # weather, temp, cloud = 'Rain', 18, 100
        # UV_API = settings.UVI_API_KEY
        # url = f'https://api.openuv.io/api/v1/uv?lat={lat}&lng={lon}'
        # headers = {'x-access-token': UV_API}
        # response = requests.get(url, headers=headers)
        # uv_data = response.json()
        # uv, uv_max = int(uv_data['result']['uv']), int(uv_data['result']['uv_max'])
        uv, uv_max = 0, 8
        now = datetime.now().time().hour
        weather = weather.lower()
        if weather == 'clear':
            if 18 < now < 8:
                weather = 'night-clear'
            else:
                weather = 'day-sunny'
        elif weather == 'drizzle':
            weather = 'sleet'
        elif weather == 'Squall':
            weather = 'cloudy-windy'
        elif weather == 'mist' and 'smoke' and 'haze' and 'dust':
            weather = 'fog'
        elif weather == 'clouds':
            weather = 'cloudy'
        now_icon = now
        if now > 12:
            now_icon = now-12
        return Response(status=status.HTTP_200_OK, template_name='main/weather.html', data={"uv": uv, 'pk': pk,
                                                                                            'uv_max': uv_max,
                                                                                            'weather': weather,
                                                                                            'cloud': cloud,
                                                                                            'temp': temp,
                                                                                            'region': region,
                                                                                            'now': now,
                                                                                            'now_icon': now_icon,})
class Review_make(APIView): # 댓글 생성
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request, pk):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        user = User.objects.get(id=user_check)
        review_set = Review_Serializer(data=request.data, context={'user': user})
        if review_set.is_valid():
            post_review = review_set.save()
            post.post_review.add(post_review)
            post.save()
            return redirect('summer_spot:post',pk)
        else:
            return Response(status=status.HTTP_200_OK, template_name='main/post.html', data={"post": post, 'pk': pk,
                                                                                             'review': review_set})
class Many_image(APIView): # 피드용 이미지

    def post(self, request, pk):
        images = Many_image_Serializer(data=request.data)
        if images.is_valid():
            check_image = images.save()
            print(check_image)
            post = Post.objects.get(id=pk)
            post.post_image.add(check_image)
            post.save()
            return redirect('summer_spot:post', pk)
        else:
            return redirect('summer_spot:post', pk)

class Post_retouch(APIView): # 피드 수정
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        post_check = Post_Serializer(instance=post)
        post_cat = Post_Categories_Serializer(instance=post)
        return Response(status=status.HTTP_200_OK, template_name='main/post_retouch.html', data={"post": post_check,
                                                                                                 'post_cat':post_cat,
                                                                                                 'pk': pk})

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        post_check = Post_Serializer(post, data=request.data)
        if post_check.is_valid():
            post_check.save()
            return redirect('summer_spot:post', pk)
        else:
            va = post_check.errors
            error = []
            for key, value in va.items():
                A = [key, value[0]]
                error.append(A)
            return Response(status=status.HTTP_200_OK, template_name='main/post_retouch.html',
                                data={"post": post_check, 'pk': pk, 'error': error})

class Post_images_del(APIView): # 피드 이미지 삭제
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, pk2):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        post.post_image.get(id=pk2).delete()
        return redirect('summer_spot:post', pk)

class Review_del(APIView): # 피드 댓글 삭제

    def get(self, request, pk, pk2):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        post.post_review.get(id=pk2).delete()
        return redirect('summer_spot:post', pk)

class Post_del(APIView): # 포스트 삭제
    def get(self, request, pk):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        Post.objects.get(id=pk).delete()
        return redirect('summer_spot:main_page')

class Post_list_make(APIView): # 포스트 리스트 만들기
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        form = Post_list_Serializer()
        return Response(status=status.HTTP_200_OK, template_name='main/post_list_make.html',
                        data={"form": form, 'pk': pk})

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        form = Post_list_Serializer(data=request.data)
        if form.is_valid():
            post_list = form.save()
            post.post_list.add(post_list)
            post.save()
            return redirect('summer_spot:post', pk)
        else:
            va = form.errors
            error = []
            for key, value in va.items():
                A = [key, value[0]]
                error.append(A)
            return Response(status=status.HTTP_200_OK, template_name='main/post_list_make.html',
                            data={"form": form, 'pk': pk, 'error':error})
class Post_list_retouch(APIView): # 피드 리스트 수정
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, pk2):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        post_list = post.post_list.get(id=pk2)
        post_check = Post_list_Serializer(instance=post_list)
        return Response(status=status.HTTP_200_OK, template_name='main/post_list_retouch.html', data={"form": post_check,
                                                                                                      'pk': pk,
                                                                                                      'pk2': pk2})

    def post(self, request, pk, pk2):
        post = Post.objects.get(id=pk)
        post_list = post.post_list.get(id=pk2)
        post_list_check = Post_list_Serializer(post_list, data=request.data)
        if post_list_check.is_valid():
            post_list_check.save()
            return redirect('summer_spot:post_list', pk, pk2)
        else:
            va = post_list_check.errors
            error = []
            for key, value in va.items():
                A = [key, value[0]]
                error.append(A)
            return Response(status=status.HTTP_200_OK, template_name='main/post_list_retouch.html',
                            data={"form": post_list_check, 'pk': pk, 'pk2': pk2, 'error': error})

class Post_list(APIView): # 선택한 피드 리스트
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk, pk2):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        post_list = post.post_list.get(id=pk2)
        # output_text = post_list.list_content.replace('\n', '<br>')
        # output_text = html.escape(output_text)
        return Response(status=status.HTTP_200_OK, template_name='main/post_list.html',
                        data={"post_list": post_list, 'pk': pk, 'pk2': pk2, 'user_check':user_check})

class Post_list_del(APIView): # 선택한 피드 리스트 삭제

    def get(self, request, pk, pk2):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        post.post_list.get(id=pk2).delete()
        post.save()
        return redirect('summer_spot:post', pk)

class Weather_search(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        return Response(status=status.HTTP_200_OK, template_name='lion_2/weather.html')
