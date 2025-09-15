from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import Group
from .models import Course, Lesson, Subscription
from users.models import User


class MaterialsTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        self.moderator = User.objects.create_user(
            email='moderator@test.com',
            password='modpass123'
        )

        # Создаем группу модераторов и добавляем пользователя
        moderators_group, created = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(moderators_group)

        # Создаем курс и урок
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            video_url='https://www.youtube.com/watch?v=test',
            owner=self.user
        )

    def test_get_courses_list(self):
        """Тестирование получения списка курсов"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson_authenticated(self):
        """Тестирование создания урока аутентифицированным пользователем"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Lesson',
            'description': 'New Lesson Description',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=new'
        }
        response = self.client.post('/api/lessons/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_unauthenticated(self):
        """Тестирование создания урока неаутентифицированным пользователем"""
        data = {
            'title': 'New Lesson',
            'description': 'New Lesson Description',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=new'
        }
        response = self.client.post('/api/lessons/create/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_youtube_validation(self):
        """Тестирование валидации YouTube ссылок"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Invalid Lesson',
            'description': 'Invalid Lesson Description',
            'course': self.course.id,
            'video_url': 'https://vk.com/video123'  # Не YouTube ссылка
        }
        response = self.client.post('/api/lessons/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Разрешены только ссылки на YouTube', str(response.data))

    def test_subscription_flow(self):
        """Тестирование функционала подписки"""
        self.client.force_authenticate(user=self.user)

        # Добавляем подписку
        response = self.client.post('/api/subscription/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Удаляем подписку
        response = self.client.post('/api/subscription/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_course_with_subscription_info(self):
        """Тестирование отображения информации о подписке в курсе"""
        self.client.force_authenticate(user=self.user)

        # Сначала проверяем без подписки
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_subscribed'])

        # Добавляем подписку и проверяем снова
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])


class PaginationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )

        # Создаем несколько курсов для тестирования пагинации
        for i in range(10):
            Course.objects.create(
                title=f'Course {i}',
                description=f'Description {i}',
                owner=self.user
            )

    def test_pagination(self):
        """Тестирование пагинации"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 5)  # page_size = 5