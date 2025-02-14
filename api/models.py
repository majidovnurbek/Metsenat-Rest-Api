from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from api.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Administrator'),
        ('sponsor', 'Sponsor'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar/student", default="../media/avatar/student/default-student.webp")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'university'
        verbose_name_plural = 'universities'


class Student(models.Model):
    class StudentTypes(models.TextChoices):
        BACHELOR = "bachelor"
        MASTER = "master"

    full_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=50, choices=StudentTypes.choices)
    contract_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    university = models.ForeignKey("api.University", on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'


class Sponsor(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROCESS = 'in_process', 'In process'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    class SponsorStatus(models.TextChoices):
        JURIDICAL = 'yuridik', 'Yuridik shaxs'
        INDIVIDUAL = 'jismoniy', 'Jismoniy shaxs'

    sponsor_full_name = models.CharField(max_length=250)
    student_sponsor = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sponsors")
    phone = models.CharField(max_length=30)
    amount = models.PositiveBigIntegerField()
    progress = models.CharField(max_length=30, choices=StatusChoices.choices)
    sponsor_status = models.CharField(max_length=50, choices=SponsorStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    organization_name = models.CharField(max_length=250, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.sponsor_status == self.SponsorStatus.INDIVIDUAL:
            self.organization_name = None  # Jismoniy shaxs bo'lsa, tashkilot nomini o'chiramiz
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.organization_name if self.organization_name else 'Jismoniy shaxs'}) - {self.amount} UZS"

    class Meta:
        verbose_name = 'sponsor'
        verbose_name_plural = 'sponsors'


class StudentSponsor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.sponsor} - {self.amount} UZS"

    class Meta:
        verbose_name = 'student sponsor'
        verbose_name_plural = 'student sponsors'
