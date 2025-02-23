from warnings import filters
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from .models import User,Student,Sponsor,StudentSponsor,PaymentSummary
from django.conf import settings
from django.db import models



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

    def get_amount_spent(self, obj):
        return obj.sponsor.amount if obj.sponsor else None

    def get_contract_amount(self, obj):
        return obj.student.contract_price if obj.student else None

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['full_name','phone','progress','organization_name','sponsor_status']

class AddStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name','phone_number','degree','contract_price','university']

class PaymentSummarySerializer(serializers.ModelSerializer):
    total_paid = serializers.SerializerMethodField()
    total_requested = serializers.SerializerMethodField()
    total_needed = serializers.SerializerMethodField()

    class Meta:
        model = PaymentSummary
        fields = ['total_paid', 'total_requested', 'total_needed', 'created_at']

    def get_total_paid(self, obj):
        return Sponsor.objects.aggregate(total_paid=models.Sum('amount'))['total_paid'] or 0

    def get_total_requested(self, obj):
        return Student.objects.aggregate(total_requested=models.Sum('contract_price'))['total_requested'] or 0

    def get_total_needed(self, obj):
        total_requested = self.get_total_requested(obj)
        total_paid = self.get_total_paid(obj)
        return total_requested - total_paid

class SponsorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['full_name','phone','amount','progress','organization_name','sponsor_status']

class StudentaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name','phone_number','degree','contract_price','university']

