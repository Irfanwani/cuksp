from django.contrib import admin
from .models import Address, Categories, Education, Experience, PasswordCodes, Profile, Projects, User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Projects)
admin.site.register(Address)
admin.site.register(Categories)
admin.site.register(PasswordCodes)