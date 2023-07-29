from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import User, Profile
from rest_framework.authtoken.models import Token
from slugify import slugify
@receiver(post_save,sender=User)
def create_token(instance,sender,created=False,*args,**kwargs):
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance,slug=slugify(instance.username))