from collections import Counter
from itertools import groupby

from django.db.models import Count, F, Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import Post_Serializer,Post_Categories_Serializer, Review_Serializer, Many_image_Serializer
from .models import Post
from user_set.models import User, User_Categories


class Post_make(APIView): # 휴양지 게시판 만들기
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post_Serializer()
        post_cat = Post_Categories_Serializer()
        return Response(status=status.HTTP_200_OK, template_name='main/post_make.html',
                        data={'post': post, 'post_cat': post_cat})

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
            error = str(post.errors)
            return Response(status=status.HTTP_200_OK, template_name='main/post_make.html',
                            data={'post': post, 'error': error})

class Main_page(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        user = User.objects.get(id=user_check)
        user_re = User_Categories.objects.filter(user=user_check)
        post_re = Post.objects.all()

        main_table_values = user_re.values()
        post_table_values = post_re.values()
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

            return Response(status=status.HTTP_200_OK, template_name='main/main_page.html', data={"post": posts})

        else:
            return Response(status=status.HTTP_200_OK, template_name='main/main_page.html', data={"post": post_re.values()})

class Select_post(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        post.user_check += 1
        post.save()
        review_set = Review_Serializer(data=request.data)
        return Response(status=status.HTTP_200_OK, template_name='main/post.html', data={"post": post, 'pk': pk,
                                                                                         'review': review_set,
                                                                                         'check_user': user_check})

class Review_make(APIView):
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
class Many_image(APIView):

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

