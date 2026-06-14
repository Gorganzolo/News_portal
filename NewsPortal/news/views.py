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
from .forms import CommentForm

class PostDetailView(DetailView):
    model = Post
    template_name = 'news_view/news_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

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
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import PostForm

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_view/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = Post.news # 'NW'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_view/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice = Post.article # 'AR'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class NewsUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_view/post_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author.user == self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(choice=Post.news)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class ArticleUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_view/post_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author.user == self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(choice=Post.article)

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class NewsDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'news_view/post_delete.html'
    success_url = reverse_lazy('news_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author.user == self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(choice=Post.news)

class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'news_view/post_delete.html'
    success_url = reverse_lazy('news_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author.user == self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(choice=Post.article)

# Профиль и авторизация
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from .models import Author
from django.contrib.auth.models import User
from .forms import UserUpdateForm

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'news_view/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_author = self.request.user.groups.filter(name='authors').exists()
        context['is_author'] = is_author

        if is_author:
            # Пытаемся получить профиль Author, чтобы вывести посты текущего пользователя
            try:
                author_profile = Author.objects.get(user=self.request.user)
                context['user_posts'] = Post.objects.filter(author=author_profile).order_by('-data_created')
            except Author.DoesNotExist:
                context['user_posts'] = []

        return context

@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        user.groups.add(authors_group)
        # Также создаем запись Author, чтобы пользователь мог создавать посты
        Author.objects.get_or_create(user=user)
    return redirect('profile')

# Лайки и дизлайки
from django.shortcuts import get_object_or_404, redirect

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.like()
    return redirect('news_detail', pk=pk)

def dislike_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.dislike()
    return redirect('news_detail', pk=pk)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.link_comment = post
            comment.author_of_comment = request.user
            comment.save()
    return redirect('news_detail', pk=pk)
