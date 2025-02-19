from api.models import User,StudentSponsor,Student,Sponsor
from api.serializers import RegisterSerializer,LoginSerializer,StudentSponsorSerializer,StudentSerializer,SponsorSerializer,AddStudentSerializer
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
    @extend_schema(
        summary='User register',
        request=RegisterSerializer,
        responses={
            200: OpenApiParameter(name="Token",description='Get token'),
            400: OpenApiParameter(name="errors",description='Get token'),
        },
        tags=['register autication'],
    )
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
    @extend_schema(
        summary='User login',
        description='Login useing email,username and password',
        request=LoginSerializer,
        responses={
            200: OpenApiParameter(name="Token",description='Get token'),
            400: OpenApiParameter(name="errors",description='Get token'),
        },
        tags=['Login autication'],
    )
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



class StudentSponsorAPIView(APIView):
    def get(self, request):
        sponsors = StudentSponsor.objects.all()
        serializer = StudentSponsorSerializer(sponsors, many=True)
        return Response(serializer.data)

class StudentAPIView(APIView):
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)

class SponsorAPIView(APIView):
    def get(self, request):
        sponsors = Sponsor.objects.all()
        serializer = SponsorSerializer(sponsors, many=True)
        return Response(serializer.data)

class AddStudentAPIView(APIView):
    @extend_schema(
        summary='add student',
        description='add student',
        request=AddStudentSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Get token'),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = AddStudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
