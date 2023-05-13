from django.db import models
from user_set.models import User, User_Categories
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    comment = models.CharField(max_length=100, blank=True)
    like = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(5)], default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

class Many_image(models.Model):
    images = models.ImageField(upload_to='post')
    images_name = models.CharField(max_length=10, blank=True)

class Post(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=50, blank=True)  # 지역
    place = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title_image = models.ImageField(upload_to='title', null=True, blank=True)
    user_check = models.IntegerField(default=0)
    post_review = models.ManyToManyField(Review, blank=True, related_name="post_review")
    post_image = models.ManyToManyField(Many_image, blank=True, related_name="post_image")
    AMBIENCE = (
        ('1', '신선한'),
        ('2', '조용한'),
        ('3', '왁자지껄한'),)
    ambience = models.CharField(verbose_name='분위기', max_length=1, choices=AMBIENCE, blank=True)
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
        ('2', '오리발'),
        ('2', '매트'),)
    rental_item = models.CharField(verbose_name='대여 물품', max_length=1, choices=RENTAL_ITEM, blank=True)

