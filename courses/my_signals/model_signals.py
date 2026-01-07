from django.db.models.signals import pre_save
from django.dispatch import receiver
from courses import models

@receiver(pre_save, sender=models.Course)
def clean_course_title(sender, instance, **kwargs):
    if instance.title:
        instance.title = instance.title.strip()
        print(f"SIGNAL: Title cleaned for course: {instance.title}")