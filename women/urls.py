from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="about"),
    path("categories/<str:cat_id>", views.categories, name="categories"),
    path("archive/<int:year>", views.archive, name="archive"),
]
