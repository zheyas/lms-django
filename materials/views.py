from rest_framework import viewsets, generics
from .models import Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Subscription
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Course
stripe.api_key = settings.STRIPE_SECRET_KEY
from rest_framework import generics
from .models import Lesson
from .serializers import LessonSerializer
from .permissions import LessonCoursePermission

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [LessonCoursePermission]

class BuyCourseAPIView(APIView):
    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=404)

        # 1. Создать продукт (если нужно, можно сохранить stripe_product_id в модели курса)
        product = stripe.Product.create(name=course.name)

        # 2. Создать цену для продукта (например, 10 usd)
        price = stripe.Price.create(
            product=product.id,
            unit_amount=1000,  # цена в центах, т.е. $10.00
            currency="usd",
        )

        # 3. Создать checkout-сессию
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price.id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/', # < URL успеха
            cancel_url='http://127.0.0.1:8000/cancel/',   # <и отмены>
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


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Добавляем в контекст объект request (по умолчанию DRF это уже делает)
        context['request'] = self.request
        # Можно добавить любые свои данные, например:
        context['extra_message'] = "Привет от ViewSet!"
        return context


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer