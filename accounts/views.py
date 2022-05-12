from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.models import Profile
from .serializers import ProfileSerializer, RegistrationSerializer, LoginSerializer, UserSerializer
from knox.models import AuthToken
from rest_framework.generics import GenericAPIView


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        _, token = AuthToken.objects.create(user)

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


class LoginView(GenericAPIView):
    serializer_class  = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        _, token = AuthToken.objects.create(user)

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = serializer.save()

        return Response({
            'profile': ProfileSerializer(profile, context=self.get_serializer_context()).data
        })

    def put(self, request):
        serializer = self.get_serializer(Profile.objects.get(id=request.user.id), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        profile = serializer.save()

        return Response({
            'profile': ProfileSerializer(profile, context=self.get_serializer_context()).data
        })