from django.shortcuts import render
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class user_name(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        return Response(status=status.HTTP_200_OK, template_name='user_name/name_make.html')

    def post(self, request):

