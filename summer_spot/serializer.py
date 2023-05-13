from rest_framework import serializers
from .models import Post, Review, Many_image


class Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title_image', 'place', 'ambience', 'personnel', 'view', 'good_place', 'rental_item')

    def create(self, validated_data):
        users = self.context.get('user')
        region_set = validated_data['place'].split()
        bool = Post.objects.create(place=validated_data['place'],
                                   region=region_set[0],
                                   user=users,
                                   title_image=validated_data['title_image'],
                                   ambience=validated_data['ambience'],
                                   personnel=validated_data['personnel'],
                                   view=validated_data['view'],
                                   good_place=validated_data['good_place'],
                                   rental_item=validated_data['rental_item'],
                                   )
        return bool


class Post_Categories_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('ambience', 'personnel', 'view', 'good_place', 'rental_item')


class Review_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        users = self.context.get('user')
        bool = Review.objects.create(comment=validated_data['comment'],
                                   user=users,
                                   like=validated_data['like'],
                                   )
        return bool

class Many_image_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Many_image
        fields = '__all__'