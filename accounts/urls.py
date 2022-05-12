from django.urls import path, include
from .views import EducationView, RegistrationView, LoginView, ProfileView, ExperienceView


urlpatterns = [
    path('', include('knox.urls')),
    path('register', RegistrationView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', ProfileView.as_view()),
    path('experience', ExperienceView.as_view()),
    path('education', EducationView.as_view()),
]