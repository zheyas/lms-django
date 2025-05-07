from django.core.exceptions import PermissionDenied
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Course, Lesson
from .paginators import StandardResultsSetPagination
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .permissions import IsOwnerOrReadOnly, ModeratorCourseLessonPermission
from .serializers import CourseSerializer, LessonSerializer


class LessonListCreate(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorCourseLessonPermission]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(course__owner=user)

    def perform_create(self, serializer):
        course_id = self.request.data.get("course")
        # Позволять создавать, только если владелец курса - текущий пользователь (и не модератор)
        if not self.request.user.groups.filter(name="moderators").exists():
            from materials.models import Course

            course = Course.objects.get(id=course_id)
            if course.owner != self.request.user:
                raise PermissionDenied("Not your course!")
        serializer.save()


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ModeratorCourseLessonPermission]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(course__owner=user)


from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Subscription


class SubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        subs = Subscription.objects.filter(user=user, course=course)
        if subs.exists():
            subs.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "подписка добавлена"
        return Response({"message": message})


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Опционально: только аутентифицированные создают/изменяют

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request  # <--- добавить эту строку!
        return context
