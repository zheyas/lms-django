
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, BuyCourseAPIView, SubscribeAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subscription/', SubscribeAPIView.as_view(), name='subscription'),
    path('courses/<int:course_id>/buy/', BuyCourseAPIView.as_view(), name='buy_course'),
]
