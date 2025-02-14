from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from api.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('student', 'Student'),
        ('admin', 'Administrator'),
        ('sponsor', 'Sponsor'),
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_staff = models.BooleanField(_('staff'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email


class OTM(models.Model):
    name = models.CharField(_('OTM nomi'), max_length=150)

    def __str__(self):
        return self.name


class Student(models.Model):
    STUDENT_TYPES = [
        ('bakalavr', 'Bakalavr'),
        ('magistr', 'Magistr'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    otm = models.ForeignKey(OTM, on_delete=models.CASCADE, related_name='students')
    created_date = models.DateField(auto_now_add=True)
    student_type = models.CharField(choices=STUDENT_TYPES, default='bakalavr', max_length=50)
    contract_amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.full_name


class Sponsor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255, blank=True, null=True)  # Yur. shaxslar uchun
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name or self.user.email


class Sponsorship(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name="sponsorships")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sponsorships")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor} → {self.student} ({self.amount} UZS)"
