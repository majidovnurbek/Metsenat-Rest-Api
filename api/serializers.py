from warnings import filters
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from .models import User,Student,Sponsor,StudentSponsor
from django.conf import settings


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','role']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name','degree','contract_price','university']

class StudentSponsorSerializer(serializers.ModelSerializer):
    contract_amount = serializers.SerializerMethodField()
    amount_spent = serializers.SerializerMethodField()

    class Meta:
        model = StudentSponsor
        fields = ['student', 'sponsor', 'contract_amount', 'amount_spent', 'created_at']

    def get_contract_amount(self, obj):
        return obj.sponsor.amount if obj.sponsor else None

    def get_amount_spent(self, obj):
        return obj.student.contract_price if obj.student else None

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['full_name','phone','progress','organization_name','sponsor_status']

class AddStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name','phone_number','degree','contract_price','university']

class SponsorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['full_name','phone','progress','organization_name','sponsor_status']

class StudentaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name','phone_number','degree','contract_price','university']

