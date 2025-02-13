from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from api.managers import UserManager
from django.core.mail import send_mail


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
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='user')
    # avatar = models.ImageField(upload_to="avatar/student", default="./student.webp")
    is_staff = models.BooleanField(_('staff'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class OTM(models.Model):
    otm_name = models.CharField(_('OTM name'), max_length=150)

class Student(models.Model):
    student_choices=[
        ('bakalavr', 'Bakalavr'),
        ('Magistr', 'Magistr'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11)
    otms = models.ForeignKey(OTM, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True,editable=True)
    student_type=models.CharField(choices=student_choices, default='bakalavr', max_length=150)
    amount_contract = models.DecimalField(max_digits=10, decimal_places=2)

class Sponsor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_full_name=models.ForeignKey(Student,on_delete=models.CASCADE)
    amount_sponsor=models.DecimalField(decimal_places=2, max_digits=10)
    created_date = models.DateField(auto_now_add=True)



class StudentSponsor(models.Model):
    student= models.ForeignKey(Student, on_delete=models.CASCADE)
    sponsor=models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    
