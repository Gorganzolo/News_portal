from django.urls import path
from .views import (
    PostListView, PostDetailView, PostSearchView,
    NewsCreateView, NewsUpdateView, NewsDeleteView,
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView,
    like_post, dislike_post, ProfileView, become_author
)

urlpatterns = [
    # Профиль (У Allauth по умолчанию LOGIN_REDIRECT_URL = '/accounts/profile/')
    # Мы переопределяем его на уровне news
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/become-author/', become_author, name='become_author'),

    # Пути для новостей
    path('', PostListView.as_view(), name='news_list'),
    path('search/', PostSearchView.as_view(), name='news_search'),
    path('<int:pk>/', PostDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),

    # Лайки и дизлайки
    path('<int:pk>/like/', like_post, name='like_post'),
    path('<int:pk>/dislike/', dislike_post, name='dislike_post'),

    # Пути для статей (префикс 'news/' убирается на уровне NewsPortal/urls.py)
    # Обратите внимание: в задании указаны пути /articles/...
    # Поэтому мы вынесем их в отдельный файл articles_urls.py или добавим префикс прямо здесь,
    # но так как этот файл подключается по пути 'news/', то пути получатся 'news/articles/...'.
    # Чтобы сделать пути точно по заданию (/articles/...), добавим их в основной urls.py.
]
