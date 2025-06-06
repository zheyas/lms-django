#materials/serializers.py
from rest_framework import serializers
from .models import  Lesson
from rest_framework import serializers
from .models import Course, Subscription

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'link')


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'lessons')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    def get_lesson_count(self, obj):
        # obj = экземпляр курса
        return obj.lessons.count()
