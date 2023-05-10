from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import User_Serializer
from .models import User

class nickname_set(APIView): #유저 만들기
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response(status=status.HTTP_200_OK, template_name='account/name_make.html')

    def post(self, request):
        form = User_Serializer(data=request.data)
        if form.is_valid():
            form.save()
            return redirect('user_set:login')
        else:
            return Response(status=status.HTTP_200_OK, template_name='account/name_make.html')

class login(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK, template_name='account/login.html')
    def post(self, request):
        try:
            user_check = User.objects.get(username=request.data['username'])
        except:
            error = "유저가 존재하지 않습니다."
            return Response(status=status.HTTP_200_OK, template_name='account/login.html', data={"error": error})
        request.session['user'] = user_check
        return redirect('main:main_page')
