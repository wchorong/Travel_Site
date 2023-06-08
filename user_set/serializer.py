from rest_framework import serializers
from .models import User


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


