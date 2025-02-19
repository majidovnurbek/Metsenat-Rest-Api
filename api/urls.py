from django.urls import path
from api.views import RegisterAPIView, LoginAPIView, UniversityAPIView, StudentSponsorAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(),name='register'),
    path('login/', LoginAPIView.as_view(),name='login'),
    path('university/', UniversityAPIView.as_view(),name='university'),
    path('student-sponsor/', StudentSponsorAPIView.as_view(),name='studentsponsor'),
]