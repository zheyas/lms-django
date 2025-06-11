#materials/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Lesson, Course, Subscription
from .serializers import LessonSerializer, CourseSerializer
from materials.permission import LessonCoursePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, LessonCoursePermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['extra_message'] = "Привет от ViewSet!"
        return context

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, LessonCoursePermission]

class BuyCourseAPIView(APIView):
    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=404)

        product = stripe.Product.create(name=course.name)
        price = stripe.Price.create(
            product=product.id,
            unit_amount=1000,
            currency="usd",
        )
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price.id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )

        return Response({'checkout_url': session.url})

class SubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        subs = Subscription.objects.filter(user=user, course=course)
        if subs.exists():
            subs.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'
        return Response({'message': message})
