
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    ordering = '-data_created'
    template_name = 'news_view/news_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'news_view/news_detail.html'
    context_object_name = 'post'