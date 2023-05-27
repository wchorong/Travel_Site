from rest_framework import serializers
from .models import Post, Review, Many_image, Post_list


class Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title_image', 'place', 'ambience', 'personnel', 'view', 'good_place', 'rental_item',
                  'title', 'content', 'user', 'zip_code')

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
                                   title=validated_data['title'],
                                   content=validated_data['content'],
                                   zip_code=validated_data['zip_code'],
                                   )
        return bool

    def update(self, instance, validated_data):
        region_set = validated_data['place'].split()
        instance.place = validated_data.get('place', instance.place)
        instance.region = validated_data.get('region', region_set[0])
        title_image = validated_data.pop('title_image', None)
        instance.ambience = validated_data.get('ambience', instance.ambience)
        instance.personnel = validated_data.get('personnel', instance.personnel)
        instance.view = validated_data.get('view', instance.view)
        instance.good_place = validated_data.get('good_place', instance.good_place)
        instance.view = validated_data.get('view', instance.view)
        instance.rental_item = validated_data.get('rental_item', instance.rental_item)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        if title_image:
            instance.title_image = title_image
        instance.save()
        return instance


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


class Post_list_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post_list
        fields = '__all__'

    def create(self, validated_data):
        bool = Post_list.objects.create(list_title=validated_data['list_title'],
                                     list_content=validated_data['list_content'],
                                     list_image=validated_data['list_image'],
                                     list_place=validated_data['list_place'],
                                     division=validated_data['division'],
                                     )
        return bool

    def update(self, instance, validated_data):
        instance.list_title = validated_data.get('list_title', instance.list_title)
        instance.list_content = validated_data.get('list_content', instance.list_content)
        list_image = validated_data.pop('list_image', None)
        instance.list_place = validated_data.get('list_place', instance.list_place)
        instance.division = validated_data.get('division', instance.division)
        if list_image:
            instance.list_image = list_image
        instance.save()
        return instance
