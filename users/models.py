from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
import random
class User(AbstractUser):
    choices_gender = (
        ("male","male"),
        ("female","female")
    )
    email = models.EmailField(max_length=80, unique=True)
    username = models.CharField(max_length=45)
    dateBirth = models.DateField(null=True , blank=True)
    location = models.TextField(null=True , blank=True)
    gender = models.TextField(null=True , blank=True , choices=choices_gender)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    otp = models.CharField(max_length=6, null=True, blank=True)
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)] 
        code_items_for_otp = []
        
        for i in range(4):
            num = random.choice(number_list)
            code_items_for_otp.append(num)

        code_string = "".join(str(item)for item in code_items_for_otp)
        self.otp = code_string
        super().save(*args, **kwargs)
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    slug = models.SlugField()
    bio = models.TextField(null=True , blank=True)
    image = models.ImageField(upload_to='Photos/images/%y/%m/%d',null=True , blank=True)
    banner = models.ImageField(upload_to='Photos/banners/%y/%m/%d',null=True , blank=True)
    website = models.CharField(null=True , blank=True, max_length=50)
    skills = models.JSONField(null=True , blank=True)
    phoneNumber = models.IntegerField(null=True , blank=True)
    joined_at = models.DateField(auto_now_add=True)
    def email(self):
        return self.user.email
    def username(self):
        return self.user.username
    def set_email(self,email):
       print(email)
       self.user.email = email
    def __str__(self) -> str:
        return self.user.username
