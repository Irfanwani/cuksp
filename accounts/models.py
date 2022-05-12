from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

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
    bio = models.TextField(max_length= 1000, blank=True, null=True)
    first_name = models.CharField(max_length=60, default='Student')
    last_name = models.CharField(max_length=60, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    contact =models.PositiveIntegerField(blank=True, null=True)
    enrollment_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profile for {self.id} created'


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'experience added for user {self.user}'

current_year = datetime.now().year
YEAR_CHOICES = tuple([(str(i), str(i)) for i in range(current_year - 8, current_year + 9)])

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    year_of_passing =  models.CharField(choices=YEAR_CHOICES, max_length=10)
    organisation = models.CharField(max_length=100)
    score = models.FloatField()
    remarks = models.TextField(max_length=1000, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Education added for user {self.user}'


class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    project_url = models.URLField(max_length=2048)
    remarks = models.TextField(max_length=1000, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project added for user {self.user}" 