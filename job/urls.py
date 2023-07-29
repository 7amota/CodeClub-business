from django.urls import path, include
from rest_framework import routers
from .views import Job_Views

router = routers.DefaultRouter()
router.register('', Job_Views)

urlpatterns = [
    path('', include(router.urls)),
]