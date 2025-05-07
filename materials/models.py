from django.db import models
from users.models import User

class Course(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=128)
    preview = models.ImageField(upload_to='courses/previews/')
    description = models.TextField()

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=128)
    description = models.TextField()
    preview = models.ImageField(upload_to='lessons/previews/')
    video_link = models.URLField()

    def __str__(self):
        return self.title
