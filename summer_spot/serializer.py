from rest_framework import serializers
from .models import Post


class Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('region', 'image', 'ambience', 'personnel', 'view', 'good_place', 'rental_item')
    def create(self, validated_data):
        users = self.context.get('user')
        bool = Post.objects.create(region=validated_data['region'],
                                   user= users,
                                   image=validated_data['image'],
                                   ambience=validated_data['ambience'],
                                   personnel=validated_data['personnel'],
                                   view=validated_data['view'],
                                   good_place=validated_data['good_place'],
                                   rental_item=validated_data['rental_item'],
                                       )
        return bool
