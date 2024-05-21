from django.test import TestCase

from course.models import Course
from groups.models import GroupOnCourse
from users.models import User


class TestGroup(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.email = "testuser@mail.ru"
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email,
                                             is_superuser=True, is_staff=True, is_active=True)
        self.course_name = "course"
        self.course_price = 1000
        self.course = Course.objects.create(name=self.course_name, price=self.course_price)

    def test_create_group(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        data = {
            'name': 'Группа 1',
            'course': self.course.pk
        }
        response = self.client.post('/groups/create/', data=data)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(f'/groups/{GroupOnCourse.objects.all()[0].pk}/')
        self.assertEquals(response.status_code, 200)

    def test_create_group__fail(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        data = {
            'name': 'Группа 1'
        }
        response = self.client.post('/groups/create/', data=data)
        self.assertEquals(response.status_code, 200)
        all_groups = list(GroupOnCourse.objects.all())
        self.assertEquals(all_groups, [])

    def test_groups(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        response = self.client.get('/groups/')
        self.assertEquals(response.status_code, 200)

    def test_group_404(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        response = self.client.get('/groups/100/')
        self.assertEquals(response.status_code, 404)

    def test_update_group(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        data = {
            'name': 'Группа 1',
            'course': self.course.pk
        }
        response = self.client.post('/groups/create/', data=data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(GroupOnCourse.objects.all()[0].name, 'Группа 1')
        data['name'] = 'Группа 2'
        response = self.client.post(f'/groups/{GroupOnCourse.objects.all()[0].pk}/edit/', data=data)
        self.assertEquals(GroupOnCourse.objects.all()[0].name, 'Группа 2')

    def test_delete_course(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        data = {
            'name': 'Группа 1',
            'course': self.course.pk
        }
        response = self.client.post('/groups/create/', data=data)
        self.assertEquals(response.status_code, 302)
        count_groups = Course.objects.all().count()
        self.assertEquals(count_groups, 1)
        response = self.client.post(f'/groups/{GroupOnCourse.objects.all()[0].pk}/delete/', data={})
        self.assertEquals(response.status_code, 302)
        count_groups = GroupOnCourse.objects.all().count()
        self.assertEquals(count_groups, 0)
