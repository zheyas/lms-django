from django.db import models
from .validators import validate_link
from django.contrib.auth import get_user_model


User = get_user_model()
class Course(models.Model):
    name = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='lessons',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    link = models.URLField(validators=[validate_link])
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True)
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

