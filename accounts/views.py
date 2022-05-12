from datetime import datetime
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.models import Education, Experience, Profile, Projects
from .serializers import EducationSerializer, ExperienceSerializer, ProfileSerializer, ProjectSerializer, RegistrationSerializer, LoginSerializer, UserSerializer
from knox.models import AuthToken
from rest_framework.generics import GenericAPIView

#API for registration of a new user
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

# API for Logging in a user
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


#API for creating, updating, deleting and getting profile details
class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        try:
            serializer = self.get_serializer(self.get_queryset().get(id=request.user.id))

            return Response(serializer.data)
        except:
            return Response({
                'error': "There is some error. Please try again"
            }, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True

            request.data.update({'id': request.user.id, 'dob': datetime.strptime(request.data['dob'], '%d/%M/%Y').date()})

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            profile = serializer.save()

            return Response({
                'profile': self.get_serializer(profile, context=self.get_serializer_context()).data
            })
        except:
            return Response({
                "error": 'There is some error.Please try again'
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True

            request.data.update({'dob': datetime.strptime(request.data['dob'], '%d/%M/%Y').date()})
            serializer = self.get_serializer(self.get_queryset().get(id=request.user.id), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            profile = serializer.save()

            return Response({
                'profile': ProfileSerializer(profile, context=self.get_serializer_context()).data
            })
        except:
            return Response({
            'error': 'There is some error. Please try again'  
            }, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            self.get_queryset().get(id=request.user.id).delete()

            return Response({
                'message': 'Done'
            }, status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'error': 'There is some error. Please try again'
            }, status.HTTP_400_BAD_REQUEST)


# API for creating, updating, deleting and getting exps
class ExperienceView(GenericAPIView):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        try:
            serializer = self.get_serializer(self.get_queryset().filter(user=request.user), many=True)
            
            return Response(serializer.data)
        except:
            return Response({
                'error': 'There is some problem.Please try again'
            }, status.HTTP_400_BAD_REQUEST)

    
    def post(self, request):
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True

            request.data.update({'user': request.user.id, "from_date": datetime.strptime(request.data['from_date'], '%d/%M/%Y').date(), 'to_date': datetime.strptime(request.data['to_date'], '%d/%M/%Y').date()})
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            exp = serializer.save()

            return Response({
                'exp': self.get_serializer(exp, context=self.get_serializer_context()).data
            })
        except:
            return Response({
                'error': 'There is some error. Please try again'
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True
            
            request.data.update({'from_date': datetime.strptime(request.data['from_date'], '%d/%M/%Y').date(), 'to_date': datetime.strptime(request.data['to_date'], '%d/%M/%Y').date()})
            serializer = self.get_serializer(self.get_queryset().get(user=request.user, id=request.data['id']), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            exp = serializer.save()

            return Response({
                'exp': self.get_serializer(exp, context=self.get_serializer_context()).data
            })
        except:
            return Response({
                'error': "There is some error. Please try again"
            }, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            self.get_queryset().get(user=request.user, id=request.query_params['id']).delete()

            return Response({
                'message': 'Done'
            }, status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'error': 'There is some error. Please try again'
            }, status.HTTP_400_BAD_REQUEST)


#API for creating, updating, deleting and getting education status
class EducationView(GenericAPIView):
    serializer_class = EducationSerializer
    queryset = Education.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        try:
            serializer = self.get_serializer(self.get_queryset().filter(user=request.user), many=True)

            return Response(serializer.data)
        except:
            return Response({
                'error': "There is some error"
            }, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True

            request.data.update({'user': request.user.id})
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            education = serializer.save()

            return Response({
                "education": self.get_serializer(education, context=self.get_serializer_context()).data
            })
        except:
            return Response({
                'error': 'There is some error. Please try again'
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            serializer = self.get_serializer(self.get_queryset().get(user=request.user, id=request.data["id"]), data=request.data, partial=True)
            
            serializer.is_valid(raise_exception=True)

            education = serializer.save()

            return Response({
                'education':self.get_serializer(education, context=self.get_serializer_context()).data
            })
        except:
            return Response({
                "error": "There is some error. Please try again"
            }, status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        try:
            self.get_queryset().get(user=request.user, id=request.query_params['id']).delete()

            return Response({
                'message': 'Done'
            }, status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                "error": "There is some error. Please try again"
            })


#API for creating, updating, deleting and getting project details
class ProjectView(GenericAPIView):
    serializer_class = ProjectSerializer
    queryset = Projects.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        try:
            serializer = self.get_serializer(self.get_queryset().filter(user=request.user), many=True)

            return Response(serializer.data)
        except:
            return Response({
                'error': "There is some error"
            }, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True

            request.data.update({'user': request.user.id})
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            education = serializer.save()

            return Response({
                "education": self.get_serializer(education, context=self.get_serializer_context()).data
            })
        except:
            return Response({
                'error': 'There is some error. Please try again'
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            serializer = self.get_serializer(self.get_queryset().get(user=request.user, id=request.data["id"]), data=request.data, partial=True)
            
            serializer.is_valid(raise_exception=True)

            education = serializer.save()

            return Response({
                'education':self.get_serializer(education, context=self.get_serializer_context()).data
            })
        except:
            return Response({
                "error": "There is some error. Please try again"
            }, status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        try:
            self.get_queryset().get(user=request.user, id=request.query_params['id']).delete()

            return Response({
                'message': 'Done'
            }, status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                "error": "There is some error. Please try again"
            })


