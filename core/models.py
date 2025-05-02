from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    other_names     = models.CharField(max_length=150, blank=True)
    GENDER_CHOICES  = [('M','Male'),('F','Female'),('O','Other')]
    gender          = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth   = models.DateField(null=True, blank=True)
    student_id      = models.CharField(max_length=50, unique=True)
    phone           = models.CharField(max_length=20, blank=True)
    programme       = models.CharField(max_length=100, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    residence       = models.CharField(max_length=100, blank=True)
    home_residence  = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"



class ExecutiveMember(models.Model):
    name  = models.CharField(max_length=100)
    role  = models.CharField(max_length=100)
    bio   = models.TextField()
    photo = models.ImageField(upload_to='executives/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} — {self.role}"

class Event(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    date        = models.DateTimeField()
    location    = models.CharField(max_length=200)
    image       = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return self.title

class PersonalityOfTheWeek(models.Model):
    name         = models.CharField(max_length=100)
    why_selected = models.TextField()
    photo        = models.ImageField(upload_to='personalities/', blank=True, null=True)
    week_date    = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.week_date})"

class Sermon(models.Model):
    title       = models.CharField(max_length=200)
    preacher    = models.CharField(max_length=100)
    date        = models.DateField()
    media_url   = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class Member(models.Model):
    name      = models.CharField(max_length=100)
    gender    = models.CharField(max_length=10)
    phone     = models.CharField(max_length=20)
    email     = models.EmailField()
    join_date = models.DateField()
    status    = models.CharField(max_length=50)

    def __str__(self):
        return self.name
