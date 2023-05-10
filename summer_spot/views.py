from django.shortcuts import render, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView


class Post_make(APIView): # 예약 게시판 만들기
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        day = datetime.now()
        min_day = str(day.date())
        return Response(status=status.HTTP_200_OK, template_name='main/write.html', data={'min_day': min_day})

    def post(self, request):
        form = Post_check(data=request.data, context={'request': request})
        day = datetime.now()
        min_day = str(day.date())
        if form.is_valid():
            form.save(car_user=request.user, context={'request': request})
            # obj = Post.objects.filter(car_user=request.user).order_by('-id')[0]
            # obj.users.add(request.user)
            road_check(request.user, "예약 게시판 생성")
            return redirect('main:list')
        else:
            error = str(form.errors)
            return Response(status=status.HTTP_200_OK, template_name='main/write.html', data={'form': form, 'min_day': min_day, 'error' : error})
