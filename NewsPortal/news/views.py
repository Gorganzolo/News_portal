from django.views.generic import ListView, DetailView
from .models import Post

# Представление для вывода списка всех новостей
class PostListView(ListView):
    model = Post
    ordering = '-data_created' # Сортировка от новых к старым
    template_name = 'news_view/news_list.html'
    context_object_name = 'news'

# Представление для вывода конкретной новости (поста)
class PostDetailView(DetailView):
    model = Post
    template_name = 'news_view/news_detail.html'
    context_object_name = 'post'
