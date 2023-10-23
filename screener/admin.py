from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Stock, User, UserStock

admin.site.register(Stock)
admin.site.register(User, UserAdmin)
admin.site.register(UserStock)
