from api.models import User,University
from api.serializers import RegisterSerializer,LoginSerializer,UniversitySerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import filters
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema,OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser



class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            # Generate jwt

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                    'refresh': str(refresh),
                    'access': access_token,
                    'username': serializer.data
                }, status=status.HTTP_201_CREATED
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user=User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({'refresh': str(refresh), 'access': str(access_token)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UniversityAPIView(APIView):
    def get(self, request):
        universities = University.objects.all()
        serializer = UniversitySerializer(universities, many=True)
        return Response(serializer.data)

        