from api.models import User,StudentSponsor,Student,Sponsor,PaymentSummary
from api.serializers import RegisterSerializer,LoginSerializer,StudentSponsorSerializer,StudentSerializer,SponsorSerializer,AddStudentSerializer,PaymentSummarySerializer
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
    parser_classes = (MultiPartParser, FormParser)
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
    parser_classes = (MultiPartParser, FormParser)
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
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk=None):
        if pk:
            try:
                sponsor = StudentSponsor.objects.get(pk=pk)
                serializer = StudentSponsorSerializer(sponsor)
                return Response(serializer.data)
            except StudentSponsor.DoesNotExist:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        sponsors = StudentSponsor.objects.all()
        serializer = StudentSponsorSerializer(sponsors, many=True)
        return Response(serializer.data)

class StudentAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk=None):
        if pk:
            try:
                student = Student.objects.get(pk=pk)
                serializer = StudentSerializer(student)
                return Response(serializer.data)
            except Student.DoesNotExist:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class SponsorAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk=None):
        if pk:
            try:
                sponsor = Sponsor.objects.get(pk=pk)
                serializer = SponsorSerializer(sponsor)
                return Response(serializer.data)
            except Sponsor.DoesNotExist:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        sponsors = Sponsor.objects.all()
        serializer = SponsorSerializer(sponsors, many=True)
        return Response(serializer.data)

class AddStudentAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        summary="Add student",
        description="Add a new student",
        request=AddStudentSerializer,
        responses={
            201: OpenApiParameter(name="Token", description="Get token"),
            400: OpenApiParameter(name="errors", description="Validation errors"),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = AddStudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentSummaryAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        summary='Payment summary',
        request=PaymentSummarySerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Error message'),
        }
    )
    def get(self, request):
        payments = PaymentSummary.objects.all()
        serializer = PaymentSummarySerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
