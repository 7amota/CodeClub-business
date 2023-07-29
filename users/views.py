from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate
from django.core.mail import send_mail, EmailMessage

from .models import *
from .serializers import *


from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser



# Create your views here.
class RegiserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
                serializer.save()
                token, _ = Token.objects.get_or_create(user=serializer.instance)
                print(serializer.instance)
                res = {
                    "message":"Account Created .",
                    "data":serializer.data,
                    "token":token.key
                }
                return Response(res , status.HTTP_200_OK)
class LoginView(generics.CreateAPIView):
     serializer_class = AuthTokenSerializer
     def post(self, request, *args, **kwargs):
          data = request.data
          user = authenticate(email=data['email'],password=data['password'])
          if user:
               print(user.is_staff)
               token,created = Token.objects.get_or_create(user=user)
               message = {
                    "message":'User Logged in Successfully',
                    'id':token.user_id,
                    'data':UserSerializer(instance=user).data,
                    "token":token.key
               }
               return Response(message, status.HTTP_200_OK)
          else:
               message = {
                    'message':'Please check the email, password and try again'
               }
               return Response(message, status.HTTP_400_BAD_REQUEST)
class EmailRequest(generics.CreateAPIView):
     queryset = User.objects.all()
     def post(self, request, *args, **kwargs):
          if 'email' not in request.POST:
               raise ValidationError({'message':"Please insert your email"})
          email = request.data['email']
          user =self.queryset.filter(email=email).first()
          if not user:
               raise ValidationError({'message':"Email not found ."})
          email = EmailMessage('Code Club Business App', f'Your OTP is {user.otp} if you got any problem please connect with the support team',to=["bm993508@gmail.com"])
          email.send()
          message = {
               "message":'The email verfication sent successfully'
          }
          return Response(message, status.HTTP_200_OK)
class CheckOTP(generics.CreateAPIView):
     queryset = User.objects.all()
     def post(self, request, *args, **kwargs):
          if 'email' not in request.POST:
               raise ValidationError({'message':"Please insert your email"})
          email = request.data['email']
          user = self.queryset.filter(email=email).first()
          if not user:
               raise ValidationError({"message":"Please re check your email ."})
          if 'otp' not in request.POST:
               raise ValidationError({"message":"Please Insert The OTP . "})
          otp = request.data['otp']
          if user.otp != otp:
               raise ValidationError({"message":"you enterd invalid otp ."})
          message = {
               'message':"Check otp operation done successfully"
          }
          return Response(message,status.HTTP_200_OK)
class ResetPassword(generics.UpdateAPIView):
     queryset = User.objects.all()
     def put(self, request, *args, **kwargs):
          if 'password' not in request.POST or 'email' not in request.POST:
               raise ValidationError({'message': 'New password/email not found.'})
          new_passwd = request.POST['password']
          email = request.POST['email']
          user = User.objects.filter(email=email).first()
          if not user:
               raise ValidationError({"message":"Please re check the email ."})
          user.set_password(new_passwd)
          message = {
               'message':"Password Update Successfully"
          }
          return Response(message ,status.HTTP_200_OK)
class ProfileView(generics.RetrieveUpdateAPIView):
     serializer_class = ProfileSerializer
     permission_classes = [IsAuthenticated]
     authentication_classes = [TokenAuthentication]
     def retrieve(self, request, *args, **kwargs):
          profile= Profile.objects.select_related("user").get(user=request.user)
          return Response(self.serializer_class(profile).data)
     def put(self, request, *args, **kwargs):
      if 'email' in request.data:
          request.user.email = request.data['email']
          request.user.save()
      if 'username' in request.data:
           request.user.username = request.data['username']
           request.user.save()
      profile = Profile.objects.select_related("user").get(user=request.user)
      serializer = ProfileSerializer(profile, data=request.data, partial=True)
      if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
