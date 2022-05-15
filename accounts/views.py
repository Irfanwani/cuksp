from datetime import datetime
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.models import Address, Categories, Education, Experience, PasswordCodes, Profile, Projects, User
from .serializers import AddressSerializer, CategorySerializer, EducationSerializer, ExperienceSerializer, ProfileSerializer, ProjectSerializer, RegistrationSerializer, LoginSerializer, UserSerializer
from knox.models import AuthToken
from rest_framework.generics import GenericAPIView
from django.core.mail import send_mail
from django.conf import settings

import random
# Code generator function
def code_generator():
    code = random.randint(1000, 10000)
    return code


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
    

# API for updating and deleting user details
class UserUpdateView(GenericAPIView):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    def put(self, request):
        try:
            serializer = self.get_serializer(self.get_queryset().get(id=request.user.id), data=request.data, partial=True)

            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response({
                'user': self.get_serializer(user, context=self.get_serializer_context()).data
            })
        except:
            return Response({
                'error': "There is some error. Please try again."
            }, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            self.get_queryset().get(id=request.user.id).delete()

            return Response({
                'message': "Done"
            })
        except:
            return Response({
                'error': 'There is some problem. Please try again.'
            }, status.HTTP_400_BAD_REQUEST)


#API for password reset
class PasswordResetView(GenericAPIView):
    serializer_class = RegistrationSerializer
    queryset = PasswordCodes.objects.all()

    def post(self, request):
        try:
            email = request.data['email']
            try:
                User.objects.get(email=email)
            except:
                return Response({
                    'error': "There is no user registered with this email. Please provide a valid registered email."
                }, status.HTTP_406_NOT_ACCEPTABLE)

            code = code_generator()
            self.get_queryset().filter(user=User.objects.get(email=email)).delete()

            self.get_queryset().create(user=User.objects.get(email=email), code=code)
            send_mail(subject='Password reset code', message=f'Here is your passowd reset code: {code}', from_email=getattr(settings, 'DEFAULT_FROM_EMAIL'), recipient_list=[email])

            return Response({
                'message': "code send to email"
            })
        except:
            return Response({
                'error': "There is some error. Please try again"
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            email = request.data['email']
            code = request.data['code']
            db_code = self.get_queryset().get(user=User.objects.get(email=email)).code
            
            if code == db_code:
                serializer = self.get_serializer(User.objects.get(email=email), data=request.data, partial=True)

                serializer.is_valid(raise_exception=True)
                user = serializer.save()

                self.get_queryset().filter(user=User.objects.get(email=email)).delete()

                _, token = AuthToken.objects.create(user)

                return Response({
                    'user': self.get_serializer(user, context=self.get_serializer_context()).data,
                    'token': token
                })
            else:
                return Response({
                    'error': "Please provide a valid code. Provided code is incorrect"
                }, status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({
                'error': 'There is some error. Please try again'
            }, status.HTTP_400_BAD_REQUEST)


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

            try:
                category = Categories.objects.create(id=request.user, category=request.data['category'])
                cat = CategorySerializer(category).data
            except:
                return Response({
                    'error': 'Please check the CATEGORY field.'
                }, status.HTTP_400_BAD_REQUEST)

            profile = serializer.save()
            return Response({
                'profile': self.get_serializer(profile, context=self.get_serializer_context()).data,
                'category': cat
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

            category = CategorySerializer(Categories.objects.get(id=request.user)).data

            return Response({
                'profile': ProfileSerializer(profile, context=self.get_serializer_context()).data,
                'category': category
            })
        except:
            return Response({
            'error': 'There is some error. Please try again'  
            }, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            self.get_queryset().get(id=request.user.id).delete()
            Categories.objects.get(id=request.user).delete()

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


# API for creatinf, updating, deleting and getting address details
class AddressView(GenericAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        try:
            serializer = self.get_serializer(self.get_queryset().filter(user=request.user), many=True)

            return Response(serializer.data)
        except:
            return Response({
                "error":"There is some error. Please try again" 
            }, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True

            request.data.update({'user': request.user.id})
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            address = serializer.save()

            return Response({
                'address': self.get_serializer(address, context=self.get_serializer_context()).data
            })
        except:
            return Response({
                "error": "There is some error. Please try again"
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            serializer = self.get_serializer(self.get_queryset().get(user=request.user, id=request.data['id']), data=request.data, partial=True)

            serializer.is_valid(raise_exception=True)

            address = serializer.save()

            return Response({
                'address': self.get_serializer(address, context=self.get_serializer_context()).data
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
                'error': "There is some error. Please try again"
            }, status.HTTP_400_BAD_REQUEST)

