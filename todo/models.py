from django.db import models
from user.models import User

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title