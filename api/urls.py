from django.urls import path
from api.views import RegisterAPIView, LoginAPIView, StudentSponsorAPIView, StudentAPIView,SponsorAPIView,AddStudentAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(),name='register'),
    path('login/', LoginAPIView.as_view(),name='login'),
    path('student-sponsor/', StudentSponsorAPIView.as_view(),name='studentsponsor'),
    path('student/', StudentAPIView.as_view(),name='student'),
    path('sponsor/', SponsorAPIView.as_view(),name='sponsor'),
    path('student/add/', AddStudentAPIView.as_view(),name='addstudent'),

]
