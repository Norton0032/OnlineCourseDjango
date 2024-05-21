from django.test import TestCase

from course.models import Course
from users.models import User


class TestCourse(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.email = "testuser@mail.ru"
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email,
                                             is_superuser=True, is_staff=True, is_active=True)

    def test_create_course(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        data = {
            'name': 'Курс 1',
            'description': 'Описание',
            'price': 1000
        }
        response = self.client.post('/courses/create/', data=data)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(f'/courses/{Course.objects.all()[0].pk}/')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Курс 1', response.content.decode())
    def test_create_course_fail(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        data = {
            'name': 'Курс 1',
            'description': 'Описание',
            'price': 'dafads'
        }
        response = self.client.post('/courses/create/', data=data)
        self.assertEquals(response.status_code, 200)
        all_course = list(Course.objects.all())
        self.assertEquals(all_course, [])

    def test_courses(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        response = self.client.get('/courses/')
        self.assertEquals(response.status_code, 200)

    def test_course_404(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        response = self.client.get('/courses/100/')
        self.assertEquals(response.status_code, 404)

    def test_update_course(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        data = {
            'name': 'Курс 1',
            'description': 'Описание',
            'price': 1000
        }
        response = self.client.post('/courses/create/', data=data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Course.objects.all()[0].name, 'Курс 1')
        data['name'] = 'Курс 2'
        response = self.client.post(f'/courses/{Course.objects.all()[0].pk}/edit/', data=data)
        self.assertEquals(Course.objects.all()[0].name, 'Курс 2')

    def test_delete_course(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        data = {
            'name': 'Курс 1',
            'description': 'Описание',
            'price': 1000
        }
        response = self.client.post('/courses/create/', data=data)
        self.assertEquals(response.status_code, 302)
        count_courses = Course.objects.all().count()
        self.assertEquals(count_courses, 1)
        response = self.client.post(f'/courses/{Course.objects.all()[0].pk}/delete/', data={})
        self.assertEquals(response.status_code, 302)
        count_courses = Course.objects.all().count()
        self.assertEquals(count_courses, 0)
