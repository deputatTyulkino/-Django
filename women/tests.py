from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from women.models import Women


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
        
    def test_data_main(self):
        w = Women.published.all()
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], w[:5])
        
    def test_paginate_main(self):
        path = reverse('home')
        page = 1
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        w = Women.published.all()
        self.assertQuerySetEqual(
            response.context_data['posts'], 
            w[(page - 1) * paginate_by:page * paginate_by]
        )
        
    def test_content_post(self):
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['posts'].content)
            
        
    def tearDown(self):
        pass