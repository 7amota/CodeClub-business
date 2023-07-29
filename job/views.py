from django.db import IntegrityError

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.validators import ValidationError


from .paginations import JobPagintation
from .permissions import IsJobAuthor
from .models import Job
from .serializers import JobSerializer
class Job_Views(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = JobPagintation
    filterset_fields = ['category']
    def get_permissions(self):
         if self.action in ['update', 'destroy']:
            permission_classes = [IsJobAuthor]
         else:
            permission_classes = [IsAuthenticated]
         return [permission() for permission in permission_classes]
    def create(self, request, *args, **kwargs):
        try:
            job = Job(user=request.user.profile)
            serializer = self.serializer_class(job,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = {
                        'message':"created successfully",
                        'data':serializer.data
                    }
                return Response(message,status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            print(f"Caught IntegrityError: {e}")
            raise ValidationError({"message":"u already published this job ~"})
        except ValidationError as e:
            raise e
        
    def update(self, request, pk,*args, **kwargs):
        data =request.data
        print(request.user.has_perm('job.view_job'))
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance,data=data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = {'message':"update successfully ~", 'data':serializer.data}
            return Response(message,status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)