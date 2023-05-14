from django.db import models

class User(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(unique=True, max_length=50, verbose_name="닉네임") # 닉네임
    region = models.CharField(max_length=50, blank=True, verbose_name="희망 지역(예: 서울, 충남)")  # 지역
    def __str__(self):
        return self.nickname

class User_Categories(models.Model): # 카테고리
    AMBIENCE = (
        ('1', '신선한'),
        ('2', '조용한'),
        ('3', '왁자지껄한'),)
    ambience = models.CharField(verbose_name='분위기', max_length=1, choices=AMBIENCE, blank=True,)
    PERSONNEL = (
        ('1', '혼자'),
        ('2', '둘이'),
        ('3', '셋이'),
        ('4', '여러 명이'),)
    personnel = models.CharField(verbose_name='인원', max_length=1, choices=PERSONNEL, blank=True)
    VIEW = (
        ('1', '자연적인'),
        ('2', '사진 찍기 좋은'),)
    view = models.CharField(verbose_name='풍경', max_length=1, choices=VIEW, blank=True)
    GOOD_PLACE = (
        ('1', '빠지'),
        ('2', '맛집이 많은'),
        ('3', '물놀이'),
        ('4', '다이빙 장소'),)
    good_place = models.CharField(verbose_name='놀 거리', max_length=1, choices=GOOD_PLACE, blank=True)
    RENTAL_ITEM = (
        ('1', '수영복'),
        ('2', '튜브'),
        ('3', '오리발'),
        ('4', '매트'),)
    rental_item = models.CharField(verbose_name='대여 물품', max_length=1, choices=RENTAL_ITEM, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
