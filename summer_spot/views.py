from collections import Counter
from itertools import groupby

from django.db.models import Count, F, Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import Post_Serializer
from .models import Post
from user_set.models import User, User_Categories


class Post_make(APIView): # 휴양지 게시판 만들기
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        try:
            user_check = request.session.get('user')
        except:
            return redirect('user_set:login')
        post = Post_Serializer()
        return Response(status=status.HTTP_200_OK, template_name='main/post_make.html',
                        data={'post': post})

    def post(self, request):
        try:
            user_check = request.session.get('user')
        except:
            return redirect('user_set:login')
        user = User.objects.get(id=user_check)
        post = Post_Serializer(data=request.data, context={'user': user})
        if post.is_valid():
                post.save()
                return redirect('summer_spot:main_page')
        else:
            error = str(post.errors)
            return Response(status=status.HTTP_200_OK, template_name='main/post_make.html',
                            data={'form': post, 'error': error})

class Main_page(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        try:
            user_check = request.session.get('user')
        except:
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
                print(my_objects)
                posts.append(my_objects.order_by('-user_check'))

            return Response(status=status.HTTP_200_OK, template_name='main/main_page.html', data={"post": posts})

        else:
            return Response(status=status.HTTP_200_OK, template_name='main/main_page.html', data={"post": post_re.values()})

