from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory

# Регистрируем модели в админке для удобного управления

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Настройки отображения модели Автор
    list_display = ('user', 'rating')
    search_fields = ('user__username',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Настройки отображения модели Категория
    list_display = ('name_category',)
    search_fields = ('name_category',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Настройки отображения модели Публикация
    list_display = ('title_of_post', 'author', 'choice', 'data_created', 'rating_of_post')
    list_filter = ('choice', 'author', 'data_created')
    search_fields = ('title_of_post', 'text_of_post')
    date_hierarchy = 'data_created'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Настройки отображения модели Комментарий
    list_display = ('author_of_comment', 'link_comment', 'date_of_comment', 'rating_of_comment')
    list_filter = ('date_of_comment', 'author_of_comment')
    search_fields = ('comment_text',)
    date_hierarchy = 'date_of_comment'

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    # Настройки отображения промежуточной таблицы
    list_display = ('post', 'category')
