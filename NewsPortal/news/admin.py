from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory

# Регистрируем модели в админке для удобного управления

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Настройки админки для модели автора
    list_display = ('user', 'rating')
    search_fields = ('user__username',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Настройки админки для модели категории
    list_display = ('name_category',)
    search_fields = ('name_category',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Настройки админки для модели поста
    list_display = ('title_of_post', 'author', 'choice', 'data_created', 'rating_of_post')
    list_filter = ('choice', 'author', 'data_created')
    search_fields = ('title_of_post', 'text_of_post')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Настройки админки для модели комментария
    list_display = ('author_of_comment', 'link_comment', 'date_of_comment', 'rating_of_comment')
    list_filter = ('date_of_comment', 'author_of_comment')
    search_fields = ('comment_text',)

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    # Настройки админки для промежуточной модели (категория-пост)
    list_display = ('post', 'category')
