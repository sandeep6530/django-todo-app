from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Todo, AuditLog


@receiver(post_save, sender=Todo)
def todo_saved(sender, instance, created, **kwargs):
    AuditLog.objects.create(
        user = instance.user,
        action = "CREATED" if created else "UPDATED",
        todo_title = instance.title
    )

@receiver(post_delete, sender=Todo)
def todo_saved(sender, instance, **kwargs):
    AuditLog.objects.create(
        user = instance.user,
        action = "DELETED",
        todo_title = instance.title
    )
