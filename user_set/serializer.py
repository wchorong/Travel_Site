from rest_framework import serializers
from .models import User, User_Categories


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class User_Categories_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Categories
        fields =( 'ambience', 'personnel', 'view', 'good_place', 'rental_item')