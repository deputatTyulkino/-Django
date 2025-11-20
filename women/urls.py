from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('about/', views.about, name='about'),
    path("category/<slug:cat_slug>", views.ShowCategory.as_view(), name="categories"),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('post/<slug:post_slug>', views.PostDetail.as_view(), name='post'),
    path('add_page/', views.AddPage.as_view(), name='add_page'),
    path('tag/<slug:tag_slug>/', views.TagsPostList.as_view(), name='tag')
]
