from .views import SubscribeAPIView
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, CourseViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('subscription/', SubscribeAPIView.as_view(), name='subscription'),

]
