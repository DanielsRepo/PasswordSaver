from django.urls import path
from . import views

urlpatterns = [
    # path('', views.all_posts, name='all_posts'),
    path('', views.AllPostsView.as_view(), name='all_posts'),

    # path('theme/<int:pk>', views.by_theme, name = 'by_theme'),
    path('theme/<int:pk>', views.ThemeListView.as_view(), name = 'by_theme'),

    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    # path('post/new/', views.post_new, name='post_new'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),

    path('post/<pk>/edit/', views.PostEditView.as_view(), name='post_edit'),

    # path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('drafts/', views.PostDraftView.as_view(), name='post_draft_list'),

    path('post/<pk>/publish/', views.post_publish, name='post_publish'),

    path('post/<pk>/delete/', views.post_delete, name='post_delete'),
    # path('post/<pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

]