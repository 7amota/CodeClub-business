from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.exceptions import ValidationError


from .models import Job
@receiver(post_save,sender=Job)
def create_token(instance,sender,created=False,*args,**kwargs):
    if created:
        job_count = Job.objects.filter(user=instance.user).count()
        if job_count >= 3:
            raise ValidationError({'message':"you can`t have more than 3 projects ~"})