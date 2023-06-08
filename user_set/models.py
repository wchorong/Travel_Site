from django.db import models


class BaseModel(models.Model):
    modify_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
class User(BaseModel):
    nickname = models.CharField(unique=True, max_length=50, verbose_name="닉네임") # 닉네임
    MOOD = (
        ('1', '신선한'),
        ('2', '자연적인'),
        ('3', '사진 찍기 좋은'),
        ('4', '조용한'),
        ('5', '멋진'),
        ('6', '왁자지껄한'),
        ('7', '사람이 적은'),
        ('8', '새로운'),
        ('9', '호화로운'),
        ('10', '야경이 멋진'),
        ('11', '고즈넉한'),)
    mood = models.CharField(verbose_name='분위기', max_length=2, choices=MOOD, blank=True)
    PERSONNEL = (
        ('1', '1인 여행'),
        ('2', '2인 여행'),
        ('3', '3인 여행'),
        ('4', '4인 여행'),
        ('5', '5인 여행'),
        ('6', '단체 여행'),)
    personnel = models.CharField(verbose_name='여행 인원', max_length=1, choices=PERSONNEL, blank=True)
    LEISURE = (
        ('1', '빠지'),
        ('2', '다이빙'),
        ('3', '스쿠버'),
        ('4', '캠핑'),
        ('5', '해변 활동'),
        ('6', '서핑'),
        ('7', '수영'),
        ('8', '모터보트'),)
    leisure = models.CharField(verbose_name='놀거리', max_length=1, choices=LEISURE, blank=True)
    RENTAL_ITEM = (
        ('1', '수영복'),
        ('2', '튜브'),
        ('3', '오리발'),
        ('4', '파라솔'),
        ('5', '돗자리(매트)'),
        ('6', '서핑 보드'),
        ('7', '비치 베드'),)
    rental_item = models.CharField(verbose_name='대여 물품', max_length=1, choices=RENTAL_ITEM, blank=True)
    def __str__(self):
        return self.nickname

