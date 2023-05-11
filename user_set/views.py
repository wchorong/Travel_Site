from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import User_Serializer, User_Categories_Serializer
from .models import User

class Nickname_set(APIView): #유저 만들기
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        form = User_Serializer()
        form_Categories = User_Categories_Serializer()
        return Response(status=status.HTTP_200_OK, template_name='account/name_make.html', data={'form': form, 'form_Categories': form_Categories})

    def post(self, request):
        form = User_Serializer(data=request.data)
        form_Categories = User_Categories_Serializer(data=request.data)
        if form.is_valid():
            if form_Categories.is_valid():
                form.save()
                user_check = User.objects.get(nickname=request.data['nickname'])
                form_Categories.save(user=user_check)
                return redirect('user_set:login')
        else:
            return Response(status=status.HTTP_200_OK, template_name='account/name_make.html', data={'form': form})

class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        return Response(status=status.HTTP_200_OK, template_name='account/login.html')
    def post(self, request):
        try:
            user_check = User.objects.get(nickname=request.data['nickname'])
        except:
            nickname = request.data['nickname']
            error = "유저가 존재하지 않습니다."
            return Response(status=status.HTTP_200_OK, template_name='account/login.html', data={"error": error, "nickname": nickname})
        request.session['user'] = user_check.id
        return redirect('summer_spot:main_page')
