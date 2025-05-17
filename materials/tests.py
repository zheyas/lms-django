from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonCrudTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="user@example.com", password="pass")
        self.admin = User.objects.create_user(
            email="admin@example.com", password="pass", is_staff=True
        )

        self.course = Course.objects.create(name="Demo")
        self.lesson = Lesson.objects.create(
            title="Lesson 1", course=self.course, video_url="https://youtube.com/abc"
        )

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.post(
            "/api/lessons/",
            {
                "title": "Lesson 2",
                "course": self.course.id,
                "video_url": "https://youtube.com/def",
            },
        )
        self.assertEqual(res.status_code, 201)

    def test_create_lesson_invalid_url(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.post(
            "/api/lessons/",
            {
                "title": "Lesson 3",
                "course": self.course.id,
                "video_url": "https://vimeo.com/123",
            },
        )
        self.assertEqual(res.status_code, 400)


class SubscriptionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.course = Course.objects.create(name="Demo")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_subscribe_unsubscribe(self):
        # Подписка
        resp = self.client.post("/api/subscription/", {"course_id": self.course.id})
        self.assertEqual(resp.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
        # Отписка
        resp = self.client.post("/api/subscription/", {"course_id": self.course.id})
        self.assertEqual(resp.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
