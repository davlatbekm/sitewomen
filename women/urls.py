from django.urls import path, re_path, register_converter
from . import views
from . import converters



urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpost/', views.AddPage.as_view(), name='add_post'),
    path('contact/', views.contact, name='contact_us'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name="tag"),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name="edit"),
]