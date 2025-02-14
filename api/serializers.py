from warnings import filters
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from .models import User
from django.conf import settings


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','role']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']
