from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import User_Serializer
from .models import User

class Nickname_set(APIView): #유저 만들기
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        form = User_Serializer()
        return Response(status=status.HTTP_200_OK, template_name='account/name_make.html', data={'form': form})

    def post(self, request):
        form = User_Serializer(data=request.data)
        if form.is_valid():
            form.save()
            return redirect('user_set:login')
        else:
            va = form.errors
            error = []
            for key, value in va.items():
                A = [key, value[0]]
                error.append(A)
            return Response(status=status.HTTP_200_OK, template_name='account/name_make.html', data={'form': form, 'error':error})

class Login(APIView): # 로그인
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        return Response(status=status.HTTP_200_OK, template_name='lion_2/login.html')
    def post(self, request):
        try:
            user_check = User.objects.get(nickname=request.data['nickname'])
        except:
            nickname = request.data['nickname']
            error = "유저가 존재하지 않습니다."
            return Response(status=status.HTTP_200_OK, template_name='lion_2/login.html', data={"error": error, "nickname": nickname})
        request.session['user'] = user_check.id
        return redirect('summer_spot:main_page')


class User_retouch(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        user = User.objects.get(id=user_check)
        form = User_Serializer(instance=user)
        return Response(status=status.HTTP_200_OK, template_name='account/user_retouch.html', data={'form': form,
                                                                                              })
    def post(self, request):
        user_check = request.session.get('user')
        if user_check is None:
            return redirect('user_set:login')
        user = User.objects.get(id=user_check)
        form = User_Serializer(user, data=request.data)
        if form.is_valid():
            form.save()
            return redirect('user_set:login')
        else:
            va = form.errors
            error = []
            for key, value in va.items():
                A = [key, value[0]]
                error.append(A)
            return Response(status=status.HTTP_200_OK, template_name='account/user_retouch.html', data={'form': form,
                                                                                                        'error': error})