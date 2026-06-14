from django.urls import path
from .views import ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
