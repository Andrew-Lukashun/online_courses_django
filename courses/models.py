from django.db import models
from django.utils.timezone import now


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save()


    def restore(self):
        self.deleted_at = None
        self.save()


class Course(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.title

class CoursePart(BaseModel):
    course = models.ForeignKey(Course, related_name='parts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default='')

    def __str__(self):
        return self.title

class CourseTopic(BaseModel):
    part = models.ForeignKey(CoursePart, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default='')

    def __str__(self):
        return self.title

class TopicDocument(BaseModel):
    topic = models.ForeignKey(CourseTopic, related_name='documents', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='topic_documents/')

    def __str__(self):
        return self.name
