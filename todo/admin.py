from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("title", )
    list_filter = ("title", "status")