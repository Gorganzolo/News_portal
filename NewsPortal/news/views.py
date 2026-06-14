from django.views.generic import ListView, DetailView
from .models import Post

# Представление для вывода списка всех новостей
class PostListView(ListView):
    model = Post
    ordering = '-data_created' # Сортировка от новых к старым
    template_name = 'news_view/news_list.html'
    context_object_name = 'news'
    paginate_by = 10 # Постраничный вывод, по 10 новостей на страницу

# Представление для вывода конкретной новости (поста)
class PostDetailView(DetailView):
    model = Post
    template_name = 'news_view/news_detail.html'
    context_object_name = 'post'

# Представление для поиска новостей
from .filters import PostFilter

class PostSearchView(ListView):
    model = Post
    ordering = '-data_created'
    template_name = 'news_view/news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

# CRUD для новостей и статей
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostForm

class NewsCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_view/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = Post.news # 'NW'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class ArticleCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_view/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = Post.article # 'AR'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class NewsUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_view/post_edit.html'

    def get_queryset(self):
        return super().get_queryset().filter(choice=Post.news)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class ArticleUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_view/post_edit.html'

    def get_queryset(self):
        return super().get_queryset().filter(choice=Post.article)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news_view/post_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return super().get_queryset().filter(choice=Post.news)

class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'news_view/post_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return super().get_queryset().filter(choice=Post.article)
