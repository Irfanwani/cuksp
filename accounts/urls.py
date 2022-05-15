from django.urls import path, include

from .views import AddressView, EducationView, PasswordResetView, ProjectView, RegistrationView, LoginView, ProfileView, ExperienceView, UserUpdateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('knox.urls')),
    path('register', RegistrationView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', ProfileView.as_view()),
    path('experience', ExperienceView.as_view()),
    path('education', EducationView.as_view()),
    path('projects', ProjectView.as_view()),
    path('address', AddressView.as_view()),
    path('update', UserUpdateView.as_view()),
    path('resetpassword', PasswordResetView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
