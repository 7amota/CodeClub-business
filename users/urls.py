from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.RegiserView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('email_request/',views.EmailRequest.as_view()),
    path("otp_request/",views.CheckOTP.as_view()),
    path("reset_password/",views.ResetPassword.as_view()),
    path("update/",views.ProfileView.as_view(),name='profile')
]
