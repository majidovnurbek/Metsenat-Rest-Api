from api.models import User, StudentSponsor, Student, Sponsor, PaymentSummary
from api.serializers import (
    RegisterSerializer,
    LoginSerializer,
    StudentSponsorSerializer,
    StudentSerializer,
    SponsorSerializer,
    AddStudentSerializer,
    PaymentSummarySerializer,
    SponsorUpdateSerializer,
    StudentaUpdateSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import filters
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from yaml import serialize


class RegisterAPIView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @extend_schema(
        summary='User register',
        request=RegisterSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Get token'),
        },
        tags=['User autication'],
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
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @extend_schema(
        summary='User login',
        description='Login useing email,username and password',
        request=LoginSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Get token'),
        },
        tags=['User autication'],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({'refresh': str(refresh), 'access': str(access_token)},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentSponsorAPIView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @extend_schema(
        summary='Student Sponsor',
        request=StudentSponsorSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Error message'),
        }, tags=['Sponsor Api'],
    )
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
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @extend_schema(
        summary='Student Api',
        request=StudentSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Error message'),
        },
        tags=['Student Api'],
    )
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
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @extend_schema(
        summary='Student update',
        request=SponsorSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Error message'),
        },
        tags=['Sponsor Api'],
    )
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
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @extend_schema(
        summary="Add student",
        description="Add a new student",
        request=AddStudentSerializer,
        responses={
            201: OpenApiParameter(name="Token", description="Get token"),
            400: OpenApiParameter(name="errors", description="Validation errors"),
        },
        tags=['Student Api'],
    )
    def post(self, request, *args, **kwargs):
        serializer = AddStudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentSummaryAPIView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @extend_schema(
        summary='Payment summary',
        request=PaymentSummarySerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Error message'),
        },
        tags=['Payment Summary'],
    )
    def get(self, request):
        payments = PaymentSummary.objects.all()
        serializer = PaymentSummarySerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SponsorUpdateAPIView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @extend_schema(
        summary='Payment summary',
        request=SponsorUpdateSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Error message'),
        },
        tags=['Sponsor Api'],
    )
    @extend_schema(
        summary='Sponsor update',
        request=SponsorUpdateSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Error message'),
        },
        tags=['Sponsor Api'],
    )
    def put(self, request, pk=None):
        sponsor = Sponsor.objects.get(pk=pk)
        serializer = SponsorUpdateSerializer(sponsor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Sponsor update',
        request=SponsorUpdateSerializer,
        tags=['Sponsor Api'],
    )
    def delete(self, request, pk=None):
        try:
            sponsor = Sponsor.objects.get(pk=pk)
        except Sponsor.DoesNotExist:
            return Response({"error": "Sponsor not found"}, status=status.HTTP_404_NOT_FOUND)

        sponsor.delete()
        return Response({"message": "Sponsor successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class StudentUpdateAPIView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @extend_schema(
        summary='Student update',
        request=StudentaUpdateSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Error message'),
        },
        tags=['Student Api'],
    )
    def put(self, request, pk=None):
        student = Student.objects.get(pk=pk)
        serializer = StudentaUpdateSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Student update',
        request=StudentaUpdateSerializer,
        responses={
            200: OpenApiParameter(name="Token", description='Get token'),
            400: OpenApiParameter(name="errors", description='Error message'),
        },
        tags=['Student Api'],
    )
    def delete(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        student.delete()
        return Response({"message": "Student successfully deleted"}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Filters"]
)
class SponsorFilterView(ListAPIView):
    serializer_class = SponsorSerializer
    queryset = Sponsor.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['full_name', 'progress', 'sponsor_status']
    filterset_fields = ['full_name', 'progress', 'sponsor_status']


@extend_schema(
    tags=["Filters"]
)
class StudentFilterView(ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['full_name', 'degree', 'university']
    search_fields = ['full_name', 'degree', 'university']


@extend_schema(
    tags=["Filters"]
)
class StudentSponsorFilterView(ListAPIView):
    serializer_class = StudentSponsorSerializer
    queryset = StudentSponsor.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student', 'sponsor', 'created_at']
    search_fields = ['student', 'sponsor', 'created_at']


@extend_schema(
    tags=["Filters"]
)
class AddSponsorApiView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @extend_schema(
        summary="Sponsor Registration",
        description="Register a new sponsor",
        request=SponsorSerializer,  # Correctly specify the request body
        responses={
            201: OpenApiResponse(response=SponsorSerializer, description="JWT access token and refresh token"),
            400: OpenApiResponse(description="Invalid input data")
        },
        tags=["Sponsor Api"]
    )
    def post(self, request):
        serializer = SponsorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
