from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import youtube_only_validator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[youtube_only_validator], required=False, allow_blank=True
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "name", "lessons_count", "lessons", ...)

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()
