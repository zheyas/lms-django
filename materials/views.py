
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from django.http import JsonResponse

from .models import Course, Lesson, Subscription
from .permissions import IsOwnerOrReadOnly, ModeratorCourseLessonPermission
from .serializers import CourseSerializer, LessonSerializer
from .paginators import StandardResultsSetPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


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

# Stripe checkout
@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        data = json.loads(request.body)
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": data["price_id"],
                    "quantity": data.get("quantity", 1),
                }
            ],
            mode="payment",
            success_url="http://localhost:8000/success",
            cancel_url="http://localhost:8000/cancel",
        )
        return JsonResponse({"id": session.id, "url": session.url})
    return JsonResponse({"error": "POST only"}, status=400)
