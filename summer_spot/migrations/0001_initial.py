# Generated by Django 4.1 on 2023-06-07 08:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_set', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Many_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('images', models.ImageField(upload_to='post')),
                ('images_name', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('list_title', models.CharField(max_length=50)),
                ('list_content', models.CharField(blank=True, max_length=500)),
                ('list_place', models.CharField(blank=True, max_length=50)),
                ('list_place_address', models.CharField(blank=True, max_length=50)),
                ('list_place_x', models.FloatField()),
                ('list_place_y', models.FloatField()),
                ('list_image', models.ImageField(null=True, upload_to='list')),
                ('division', models.CharField(blank=True, choices=[('1', '편의 시설'), ('2', '맛집'), ('3', '볼거리'), ('4', '놀거리')], max_length=1, verbose_name='구분')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=100)),
                ('like', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='user_set.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('region', models.CharField(max_length=50)),
                ('place', models.CharField(max_length=50)),
                ('place_address', models.CharField(max_length=50)),
                ('place_x', models.FloatField()),
                ('place_y', models.FloatField()),
                ('title_image', models.ImageField(null=True, upload_to='title')),
                ('user_check', models.IntegerField(default=0)),
                ('content', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=30)),
                ('number', models.CharField(blank=True, max_length=30)),
                ('sub_title', models.CharField(blank=True, max_length=50)),
                ('mood', models.CharField(blank=True, choices=[('1', '신선한'), ('2', '자연적인'), ('3', '사진 찍기 좋은'), ('4', '조용한'), ('5', '멋진'), ('6', '왁자지껄한'), ('7', '사람이 적은'), ('8', '새로운'), ('9', '호화로운'), ('10', '야경이 멋진'), ('11', '고즈넉한')], max_length=2, verbose_name='분위기')),
                ('personnel', models.CharField(blank=True, choices=[('1', '1인 여행'), ('2', '2인 여행'), ('3', '3인 여행'), ('4', '4인 여행'), ('5', '5인 여행'), ('6', '단체 여행')], max_length=1, verbose_name='여행 인원')),
                ('leisure', models.CharField(blank=True, choices=[('1', '빠지'), ('2', '다이빙'), ('3', '스쿠버'), ('4', '캠핑'), ('5', '해변 활동'), ('6', '서핑'), ('7', '수영'), ('8', '모터보트')], max_length=1, verbose_name='놀거리')),
                ('rental_item', models.CharField(blank=True, choices=[('1', '수영복'), ('2', '튜브'), ('3', '오리발'), ('4', '파라솔'), ('5', '돗자리(매트)'), ('6', '서핑 보드'), ('7', '비치 베드')], max_length=1, verbose_name='대여 물품')),
                ('post_image', models.ManyToManyField(blank=True, related_name='post_image', to='summer_spot.many_image')),
                ('post_list', models.ManyToManyField(blank=True, related_name='post_list', to='summer_spot.post_list')),
                ('post_review', models.ManyToManyField(blank=True, related_name='post_review', to='summer_spot.review')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='user_set.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]