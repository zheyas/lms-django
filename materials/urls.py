from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonDetail, LessonListCreate, SubscribeAPIView

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreate.as_view(), name="lesson-list-create"),
    path("lessons/<int:pk>/", LessonDetail.as_view(), name="lesson-detail"),
    path("subscription/", SubscribeAPIView.as_view(), name="subscription"),
]
