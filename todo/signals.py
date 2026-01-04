from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Todo


@receiver(post_save, sender=Todo)
def todo_created(sender, instance, created, **kwargs):
    if created:
        print(f"Todo created: {instance.title}")

