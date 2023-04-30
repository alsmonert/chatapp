from django.contrib import admin
from .models import CustomUser, Jwt

# Register your models here.

# admin.site.register((Jwt,))
admin.site.register((CustomUser, Jwt))
