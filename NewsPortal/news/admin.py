from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory

# Настройки для модели Автор
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Поля для отображения в списке
    list_display = ('user', 'rating')
    # Поля для поиска
    search_fields = ('user__username',)

# Настройки для модели Категория
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_category',)
    search_fields = ('name_category',)

# Настройки для модели Публикация
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Основная информация о публикации
    list_display = ('title_of_post', 'author', 'choice', 'data_created', 'rating_of_post')
    # Боковые фильтры
    list_filter = ('choice', 'author', 'data_created')
    # Поиск по заголовку и тексту
    search_fields = ('title_of_post', 'text_of_post')

# Настройки для модели Комментарий
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_of_comment', 'link_comment', 'date_of_comment', 'rating_of_comment')
    list_filter = ('date_of_comment', 'author_of_comment')
    search_fields = ('comment_text',)

# Настройки для промежуточной таблицы Категория-Пост
@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
