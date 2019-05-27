from django.urls import path, include
from django.contrib import admin
from blog_app.forms import LoginForm
from blog_app.views import LoginView, signup

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/registration/', signup, name='registration'),
    path('', include('blog_app.urls')),
]