from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Поле choice исключено, чтобы пользователь не мог его изменять
        fields = ['author', 'category', 'title_of_post', 'text_of_post']
        labels = {
            'author': 'Автор',
            'category': 'Категории',
            'title_of_post': 'Заголовок',
            'text_of_post': 'Текст',
        }
