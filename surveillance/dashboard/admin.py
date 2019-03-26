from django.contrib import admin
from .models import SecurityCamera, ValidIdentifier

# Register your models here.

admin.site.register(SecurityCamera)
admin.site.register(ValidIdentifier)