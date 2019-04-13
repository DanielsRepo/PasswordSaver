from django import forms
from .models import Post, Theme

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