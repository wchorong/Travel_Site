from rest_framework import serializers
from .models import Post, Review, Many_image, Post_list


class Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title_image', 'place', 'personnel', 'leisure', 'mood', 'rental_item',
                  'title', 'content', 'user', 'place_x', 'place_y', 'place_address', 'number', 'sub_title')

    def create(self, validated_data):
        users = self.context.get('user')
        region_set = validated_data['place_address'].split()
        bool = Post.objects.create(place=validated_data['place'],
                                   region=region_set[0],
                                   user=users,
                                   title_image=validated_data['title_image'],
                                   leisure=validated_data['leisure'],
                                   personnel=validated_data['personnel'],
                                   mood=validated_data['mood'],
                                   rental_item=validated_data['rental_item'],
                                   title=validated_data['title'],
                                   content=validated_data['content'],
                                   place_address=validated_data['place_address'],
                                   place_x=validated_data['place_x'],
                                   place_y=validated_data['place_y'],
                                   number=validated_data['number'],
                                   sub_title=validated_data['sub_title'],
                                   )
        return bool

    def update(self, instance, validated_data):
        region_set = validated_data['place_address'].split()
        instance.place = validated_data.get('place', instance.place)
        instance.region = validated_data.get('region', region_set[0])
        title_image = validated_data.pop('title_image', None)
        instance.leisure = validated_data.get('leisure', instance.leisure)
        instance.personnel = validated_data.get('personnel', instance.personnel)
        instance.mood = validated_data.get('mood', instance.mood)
        instance.rental_item = validated_data.get('rental_item', instance.rental_item)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.place_address = validated_data.get('place_address', instance.place_address)
        instance.place_x = validated_data.get('place_x', instance.place_x)
        instance.place_y = validated_data.get('place_y', instance.place_y)
        instance.number = validated_data.get('number', instance.number)
        instance.sub_title = validated_data.get('sub_title', instance.sub_title)
        if title_image:
            instance.title_image = title_image
        instance.save()
        return instance


class Post_Categories_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('mood', 'personnel', 'leisure', 'rental_item')


class Review_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        users = self.context.get('user')
        like = validated_data.get('like', 0.0)
        bool = Review.objects.create(comment=validated_data['comment'],
                                     user=users,
                                     like=like,
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
                                        list_place_address=validated_data['list_place_address'],
                                        list_place_x=validated_data['list_place_x'],
                                        list_place_y=validated_data['list_place_y'],
                                        division=validated_data['division'],
                                     )
        return bool

    def update(self, instance, validated_data):
        instance.list_title = validated_data.get('list_title', instance.list_title)
        instance.list_content = validated_data.get('list_content', instance.list_content)
        list_image = validated_data.pop('list_image', None)
        instance.list_place = validated_data.get('list_place', instance.list_place)
        instance.division = validated_data.get('division', instance.division)
        instance.list_place_address = validated_data.get('list_place_address', instance.list_place_address)
        instance.list_place_x = validated_data.get('list_place_x', instance.list_place_x)
        instance.list_place_y = validated_data.get('list_place_y', instance.list_place_y)
        if list_image:
            instance.list_image = list_image
        instance.save()
        return instance
