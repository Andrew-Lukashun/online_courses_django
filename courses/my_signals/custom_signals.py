from django.dispatch import Signal, receiver

COURSE_SENDER = 'course'
course_published = Signal()

@receiver(course_published, sender=COURSE_SENDER)
def notify_course_published(**kwargs):
    print(f"CUSTOM SIGNAL: Course published: {kwargs.get('course')}")