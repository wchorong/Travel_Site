from rest_framework import serializers
from .models import Post, Post_Categories


class Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    def create(self, validated_data):  # @수정 완
        bool = Post.objects.create(region=validated_data['region'],
                                   user=self.context.get("request.user"),
                                   image=validated_data['image'],
                                       )
        return bool

class Post_Categories_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post_Categories
        fields = '__all__'
