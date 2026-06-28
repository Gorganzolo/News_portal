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
    # Фильтрация по рейтингу
    list_filter = ('rating',)

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
    # Поля для поиска
    search_fields = ('title_of_post', 'text_of_post')
    # Навигация по датам
    date_hierarchy = 'data_created'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Комментарий в админке.
    """
    # Показываем инфу о комментарии
    list_display = ('author_of_comment', 'link_comment', 'date_of_comment', 'rating_of_comment')
    # Фильтры сбоку
    list_filter = ('date_of_comment', 'author_of_comment')
    # Поля для поиска
    search_fields = ('comment_text',)
    # Навигация по датам
    date_hierarchy = 'date_of_comment'

# Промежуточная таблица
@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    """
    Настройки отображения промежуточной таблицы Категория поста в админке.
    """
    list_display = ('post', 'category')
