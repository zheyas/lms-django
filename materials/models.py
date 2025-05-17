from django.contrib.auth import get_user_model
from django.db import models

from users.models import User


class Course(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=128)
    preview = models.ImageField(upload_to="courses/previews/")
    description = models.TextField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.title


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=128)
    description = models.TextField()
    preview = models.ImageField(upload_to="lessons/previews/")
    video_link = models.URLField()

    def __str__(self):
        return self.title
