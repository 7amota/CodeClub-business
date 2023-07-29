from rest_framework.validators import ValidationError
from django.db import models
from users.models import User, Profile
class Job(models.Model):
    category_choices = (("programming","programming"),("design","design"),("management","management"))
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,)
    title = models.CharField(max_length=150)
    skills = models.CharField(null=True,blank=True,max_length=50)
    description = models.CharField(null=True,blank=True,max_length=50)
    budget = models.IntegerField()
    image = models.ImageField(upload_to='Photos/jobs/%y/%m/%d',null=True,blank=True)
    category = models.CharField(choices=category_choices, max_length=50,null=True,blank=True)
    time = models.CharField(null=True,blank=True,max_length=50)
    created_at = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ('user','title')
    def __str__(self):
        return f"{self.title} - {self.pk} - {self.user}"
    