from typing import Any, Optional
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Job
# Register your models here.
class JobAdmin(admin.ModelAdmin):
    model=  Job
    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.pk == 5
    def get_form(self, request, obj, **kwargs) -> Any:
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["title"].disabled = True
        return form
admin.site.register(Job,JobAdmin)