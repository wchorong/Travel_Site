from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import User_Serializer

class user_name(APIView): #유저 만들기
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response(status=status.HTTP_200_OK, template_name='user_name/name_make.html')

    def post(self, request):
        form = User_Serializer(data=request.data)
        if form.is_valid():
            form.save()
            return redirect('main:main_page')
        else:
            return Response(status=status.HTTP_200_OK, template_name='user_name/name_make.html')


