from warnings import filters
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from .models import User,Student,University,Sponsor,StudentSponsor
from django.conf import settings


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','role']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name','degree','contract_price','university']

class StudentSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSponsor
        fields = ['student','sponsor','amount','created_at']

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['full_name','phone','progress','organization_name','sponsor_status']

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id','name']