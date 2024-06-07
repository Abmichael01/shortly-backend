from rest_framework import serializers
from django.contrib.auth.models import User
from . models import Url, Click


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ["id",  "user", "url", "keyword", "clicks", "created_at"]
        extra_kwargs = {"user": {"read_only": True}}

class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ["id", "url", "ip_address", "location"]

    