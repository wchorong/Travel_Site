from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import Post_Serializer, Post_Categories_Serializer
from .models import Post, Post_Categories
from user_set.models import User, User_Categories


class Post_make(APIView): # 휴양지 게시판 만들기
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        return Response(status=status.HTTP_200_OK, template_name='main/post_write.html')

    def post(self, request):
        post = Post_Serializer(data=request.data)
        categories = Post_Categories_Serializer(data=request.data)
        if post.is_valid():
            if categories.is_valid():
                post.save(context={'request.user': request.user})
                categories.save(post=post)
                return redirect('main:main_page')
        else:
            error = str(post.errors)
            return Response(status=status.HTTP_200_OK, template_name='main/post_write.html', data={'form': post, 'error': error})

class Main_page(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        user_categories = User_Categories.objects.get(user=request.user)
