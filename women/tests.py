from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse, reverse_lazy


# Create your tests here.
class WomenTest(TestCase):
    def setUp(self):
        pass

    def test_main_page(self):
        path = reverse("home")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "women/index.html")
        self.assertEqual(response.context_data["title"], "Главная")

    def test_redirect(self):
        path = reverse('add_page')
        redirect_url = reverse_lazy('users:login') + '?next=' = path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)
        
    def tearDown(self):
        pass