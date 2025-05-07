from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from django.core.exceptions import PermissionDenied

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

from rest_framework import viewsets, mixins, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import ModeratorCourseLessonPermission, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

class LessonListCreate(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorCourseLessonPermission]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(course__owner=user)

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        # Позволять создавать, только если владелец курса - текущий пользователь (и не модератор)
        if not self.request.user.groups.filter(name='moderators').exists():
            from materials.models import Course
            course = Course.objects.get(id=course_id)
            if course.owner != self.request.user:
                raise PermissionDenied('Not your course!')
        serializer.save()

class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorCourseLessonPermission]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(course__owner=user)