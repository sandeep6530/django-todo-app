from django.db import models
from django.conf import settings
from django.utils.timezone import now

from user.models import User
from todo.managers import TodoQuerySet


class TodoManager(models.Manager):
    def get_queryset(self):
        return TodoQuerySet(self.model, using=self._db).active()

class Todo(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="user",
        db_index=True
        )
    title = models.CharField(max_length=200)
    description = models.TextField()
    STATUS_CHOICES = (
            ("pending", "Pending"),
            ("complete", "Complete"),
        )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="deleted_todos",
        on_delete=models.SET_NULL
    )

    objects = TodoManager()
    all_objects = TodoQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def soft_delete(self, user):
        self.is_deleted = True
        self.deleted_at = now()
        self.deleted_by = user
        self.save()
    

class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    action = models.CharField(max_length=50)
    object_type = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.action} - {self.object_id}"