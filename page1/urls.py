from django.urls import path
from . import views

urlpatterns = [
    path('', views.page1, name='page1'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/delete/', views.post_delete, name='post_delete'),
]