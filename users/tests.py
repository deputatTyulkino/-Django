from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your tests here.
class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.path = reverse("users:register")
        self.data = {
            "username": "test",
            "email": "a@a.ru",
            "first_name": "test",
            "last_name": "test",
            "password1": "12345QPow!",
            "password2": "12345QPow!",
        }
    
    def test_form_registartion_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register.html")

    def test_user_registration_success(self):
        user_model = get_user_model()
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(user_model.object.filter(username=self.data["username"]).exists())

    def test_user_registration_password_error(self):
        self.data['password2'] = '12345QPo'
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Passwords do not match')