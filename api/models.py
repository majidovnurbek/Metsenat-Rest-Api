from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _



class University(models.Model):
    name = models.CharField(max_length=100)





class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('sponsor', 'Sponsor'),
    )

    Certificates=(
        ('bakalavr', 'bakalavr'),
        ('magistr', 'magistr'),
    )

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True, )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    role=models.CharField(_('role'), max_length=30, choices=ROLE_CHOICES, default='user')
    avatar = models.ImageField(_('avatar'), null=True, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=30, blank=True)
    university_name=models.ForeignKey(University, on_delete=models.CASCADE)
    certificate=models.CharField(_('certificate'), max_length=30, choices=Certificates)
    contract=models.CharField(_('contract'), max_length=30)


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    
    
    
    