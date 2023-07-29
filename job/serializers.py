from rest_framework.validators import ValidationError
from rest_framework import serializers
from .models import Job
from users.models import Profile
from users.serializers import ProfileSerializer
class JobSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
     
    