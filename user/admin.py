from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "role", "is_active")
    search_fields = ("email", "username")
    readonly_fields = ("last_login", "date_joined")
    list_filter = ("role", "is_active")