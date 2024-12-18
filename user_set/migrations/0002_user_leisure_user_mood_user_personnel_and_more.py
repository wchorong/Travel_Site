# Generated by Django 4.1 on 2023-06-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_set', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='leisure',
            field=models.CharField(blank=True, choices=[('1', '빠지'), ('2', '다이빙'), ('3', '스쿠버'), ('4', '캠핑'), ('5', '해변 활동'), ('6', '서핑'), ('7', '수영'), ('8', '모터보트')], max_length=1, verbose_name='놀거리'),
        ),
        migrations.AddField(
            model_name='user',
            name='mood',
            field=models.CharField(blank=True, choices=[('1', '신선한'), ('2', '자연적인'), ('3', '사진 찍기 좋은'), ('4', '조용한'), ('5', '멋진'), ('6', '왁자지껄한'), ('7', '사람이 적은'), ('8', '새로운'), ('9', '호화로운'), ('10', '야경이 멋진'), ('11', '고즈넉한')], max_length=2, verbose_name='분위기'),
        ),
        migrations.AddField(
            model_name='user',
            name='personnel',
            field=models.CharField(blank=True, choices=[('1', '1인 여행'), ('2', '2인 여행'), ('3', '3인 여행'), ('4', '4인 여행'), ('5', '5인 여행'), ('6', '단체 여행')], max_length=1, verbose_name='여행 인원'),
        ),
        migrations.AddField(
            model_name='user',
            name='rental_item',
            field=models.CharField(blank=True, choices=[('1', '수영복'), ('2', '튜브'), ('3', '오리발'), ('4', '파라솔'), ('5', '돗자리(매트)'), ('6', '서핑 보드'), ('7', '비치 베드')], max_length=1, verbose_name='대여 물품'),
        ),
        migrations.DeleteModel(
            name='User_Categories',
        ),
    ]
