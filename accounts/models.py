from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#Creating a custom user model with some variations from the original one (like unique email, username field changed to email)

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return f'{self.username}'


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

class Profile(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dp = models.ImageField(upload_to='images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=60, default='Student')
    last_name = models.CharField(max_length=60, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    contact =models.PositiveIntegerField(blank=True, null=True)
    enrollment_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)

    def __str__(self):
        return f'Profile for {self.id} created'