from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="about"),
    path('about/', views.about, name='about'),
    path("categories/<str:cat_id>", views.categories, name="categories"),
    path('contact/', views.contact, name='contact'),
    path('post/<slug:post_slug>', views.show_post, name='post'),
    path('add_page/', views.add_page, name='add_page'),
]
