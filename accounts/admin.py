from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'resort')}),
    )
    list_display = ('username', 'email', 'role', 'resort', 'is_staff')

admin.site.register(User, CustomUserAdmin)
