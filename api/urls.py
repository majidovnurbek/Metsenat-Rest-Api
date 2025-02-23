from django.urls import path
from api.views import RegisterAPIView, LoginAPIView, StudentSponsorAPIView, StudentAPIView,SponsorAPIView,AddStudentAPIView,PaymentSummaryAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(),name='register'),
    path('login/', LoginAPIView.as_view(),name='login'),
    path('student-sponsor/', StudentSponsorAPIView.as_view(),name='studentsponsor'),
    path('student-sponsor/<int:pk>/', StudentSponsorAPIView.as_view(),name='studentsponsordetail'),
    path('student/', StudentAPIView.as_view(),name='student'),
    path('student/<int:pk>/', StudentAPIView.as_view(),name='studentdetail'),
    path('sponsor/', SponsorAPIView.as_view(),name='sponsor'),
    path('sponsor/<int:pk>/', SponsorAPIView.as_view(),name='sponsordetail'),
    path('student/add/', AddStudentAPIView.as_view(),name='addstudent'),
    path('dashboard/',PaymentSummaryAPIView.as_view(),name='dashboard'),

]
