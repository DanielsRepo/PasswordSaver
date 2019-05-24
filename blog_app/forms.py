from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Theme
from bootstrap_modal_forms.forms import BSModalForm

class PostForm(forms.ModelForm):
    # для изменения ------ в выпадающ списке
    theme = forms.ModelChoiceField(Theme.objects.all(), empty_label='Choose one of themes')
    class Meta:
        model = Post
        fields = ('title', 'text', 'theme')
    
    # или для изменения ------ в выпадающ списке
    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['theme'].empty_label = 'Choose one of themes'

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(max_length = 254, help_text = 'This field is required.')

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

    # def save(self):
    #     user = super(RegistrationForm, self).save()
    #     user.username = self.cleaned_data('username')
    #     user.email = self.cleaned_data('email')
