from .models import *
from rest_framework import serializers
from rest_framework.validators import ValidationError
class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username" , "password", "location" , "dateBirth"]
        
    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise ValidationError({"email":"Email is already used, try another one"})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio','website','joined_at','email','phoneNumber','banner','image','username','skills','slug']
    