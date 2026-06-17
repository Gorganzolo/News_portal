from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory

# Регистрируем модели в админке для удобного управления

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Автор в админке.
    """
    # Поля для отображения в списке
    list_display = ('user', 'rating')
    # Поля для поиска
    search_fields = ('user__username',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Категория в админке.
    """
    list_display = ('name_category',)
    search_fields = ('name_category',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Публикация в админке.
    """
    # Показываем ключевую информацию о посте
    list_display = ('title_of_post', 'author', 'choice', 'data_created', 'rating_of_post')
    # Фильтры сбоку
    list_filter = ('choice', 'author', 'data_created')
    search_fields = ('title_of_post', 'text_of_post')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Комментарий в админке.
    """
    # Показываем инфу о комментарии
    list_display = ('author_of_comment', 'link_comment', 'date_of_comment', 'rating_of_comment')
    list_filter = ('date_of_comment', 'author_of_comment')
    search_fields = ('comment_text',)

# Промежуточную таблицу тоже можно зарегистрировать, если нужно
@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    """
    Настройки отображения промежуточной таблицы Категория поста в админке.
    """
    list_display = ('post', 'category')
