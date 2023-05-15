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
class Post_search(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def post(self, request):
        user_check = request.session.get('user')
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
            filters = Q()  # 빈 Q 객체 생성

            if request.data['ambience']:
                filters &= Q(ambience__icontains=request.data['ambience'])

            if request.data['personnel']:
                filters &= Q(personnel__icontains=request.data['personnel'])

            if request.data['view']:
                filters &= Q(view__icontains=request.data['view'])

            if request.data['good_place']:
                filters &= Q(good_place__icontains=request.data['good_place'])

            if request.data['rental_item']:
                filters &= Q(rental_item__icontains=request.data['rental_item'])
            for grouped_mapping in grouped_queries:
                filter_condition = Q()
                for fields_mapping in grouped_mapping:
                    q_objects = Q(**fields_mapping)
                    filter_condition |= q_objects
                my_objects = Post.objects.filter(filter_condition)
                posts.append(my_objects.order_by('-user_check').filter(filters))

            print(posts)

            return Response(status=status.HTTP_200_OK, template_name='main/main_page.html', data={"post": posts})

        else:
            return Response(status=status.HTTP_200_OK, template_name='main/main_page.html',
                            data={"post": post_re.values()})


class Select_post(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        check_user = request.session.get('user')
        if check_user is None:
            return redirect('user_set:login')
        post = Post.objects.get(id=pk)
        post.user_check += 1
        post.save()
        review_set = Review_Serializer(data=request.data)
        return Response(status=status.HTTP_200_OK, template_name='main/post.html', data={"post": post, 'pk': pk,
                                                                                         'review': review_set,
                                                                                         'check_user': check_user})

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

class Post_retouch(APIView):
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
            return redirect('summer_spot:main_page')
        else:
            return Response(status=status.HTTP_200_OK, template_name='main/post_retouch.html',
                                data={"post": post_check, 'pk': pk})

class Post_images_del(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, pk2):
        post = Post.objects.get(id=pk)
        post.post_image.get(id=pk2).delete()
        return redirect('summer_spot:post', pk)

class Review_del(APIView):

    def get(self, request, pk, pk2):
        post = Post.objects.get(id=pk)
        post.post_review.get(id=pk2).delete()
        return redirect('summer_spot:post', pk)

class Post_del(APIView):
    def get(self, request, pk):
        Post.objects.get(id=pk).delete()
        return redirect('summer_spot:main_page')

class Post_list_make(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
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
            return Response(status=status.HTTP_200_OK, template_name='main/post_list_make.html',
                            data={"form": form, 'pk': pk})
class Post_list_retouch(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, pk2):
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
            print("asdasdas")
            return redirect('summer_spot:post', pk)
        else:
            return Response(status=status.HTTP_200_OK, template_name='main/post_list_retouch.html',
                            data={"form": post_list_check, 'pk': pk, 'pk2': pk2})

class Post_list(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk, pk2):
        post = Post.objects.get(id=pk)
        post_list = post.post_list.get(id=pk2)
        return Response(status=status.HTTP_200_OK, template_name='main/post_list.html',
                        data={"post_list": post_list, 'pk': pk, 'pk2': pk2})

class Post_list_del(APIView):

    def get(self, request, pk, pk2):
        post = Post.objects.get(id=pk)
        post.post_list.get(id=pk2).delete()
        post.save()
        return redirect('summer_spot:post', pk)