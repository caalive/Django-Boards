from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase


class PasswordChangeTests(TestCase):
    def setUp(self):
        username = 'john'
        password = '123abcdef'
        user = User.objects.create(username=username, email='john@code.com', password=password)
        url = reverse('password_change')
        self.client.login(userbane=username, password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve('/settings/password/')
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeView)

    def csrf_contains_form(self):
        self.assertContains(self.responsen, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestsCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create(username='john', email='john@code.com',
                                        password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='john', password='old_password')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestsCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'

             })

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        self.user.refresh_form_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestsCase):
    def tests_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))






