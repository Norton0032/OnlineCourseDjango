from django.test import TestCase
from users.models import User


class TestUsers(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.email = "testuser@mail.ru"
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email,
                                             is_superuser=True, is_staff=True, is_active=True)

    def test_redirect_without_login(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 302)
        response = self.client.get('', follow=True)
        self.assertIn('Авторизация', response.content.decode())

    def test_login_on_username(self):
        username = 'testuser'
        password = 'testpassword'
        login_successful = self.client.login(username=username, password=password)
        self.assertTrue(login_successful)

    def test_fail_login(self):
        username = 'testuser'
        password = '12345'
        login_successful = self.client.login(username=username, password=password)
        self.assertFalse(login_successful)

    def test_login_on_email(self):
        username = 'testuser@mail.ru'
        password = 'testpassword'
        login_successful = self.client.login(username=username, password=password)
        self.assertTrue(login_successful)

    def test_prifile(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_users(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        response = self.client.get('/users/')
        self.assertEquals(response.status_code, 200)

    def test_users_404(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        response = self.client.get('/users/100/')
        self.assertEquals(response.status_code, 404)

    def test_user(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        response = self.client.get(f'/users/{User.objects.all()[0].pk}/')
        self.assertEquals(response.status_code, 200)

    def test_create_user(self):
        username = 'testuser'
        password = 'testpassword'
        self.client.login(username=username, password=password)
        data = {
            'username': 'user123',
            'email': 'user123@mail.ru',
            'first_name': 'Никита',
            'last_name': 'Петров',
            'password1': '1234567890qwe',
            "password2": '1234567890qwe',
        }
        response = self.client.post('/users/create/', data=data)
        self.assertEquals(response.status_code, 302)
        login_successful = self.client.login(username=data['username'], password=data['password1'])
        self.assertTrue(login_successful)
