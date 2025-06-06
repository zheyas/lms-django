
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from .models import Course, Lesson

class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="password")
        self.client.force_authenticate(self.user)
        course = Course.objects.create(name="Course 1")
        Lesson.objects.create(course=course, name="Lesson 1", link="https://youtube.com/test")

    def test_lesson_list(self):
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)  # Проверка пагинации
