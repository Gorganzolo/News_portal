from django import forms
from django.contrib.auth.models import User
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

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        labels = {
            'comment_text': 'Текст комментария',
        }
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Оставьте свой комментарий...'}),
        }
