from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory

# Регистрируем модели в админке для удобного управления

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Поля для отображения в списке
    list_display = ('user', 'rating')
    # Поля для поиска (по имени пользователя)
    search_fields = ('user__username',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_category',)
    search_fields = ('name_category',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Показываем ключевую информацию о публикации
    list_display = ('title_of_post', 'author', 'get_choice_display', 'data_created', 'rating_of_post')
    # Фильтры сбоку для быстрой навигации
    list_filter = ('choice', 'author', 'data_created')
    # Поиск по заголовку и тексту
    search_fields = ('title_of_post', 'text_of_post')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Показываем инфу о комментарии
    list_display = ('author_of_comment', 'get_post_title', 'date_of_comment', 'rating_of_comment')
    list_filter = ('date_of_comment', 'author_of_comment')
    search_fields = ('comment_text',)

    # Метод для получения названия поста в списке комментариев
    def get_post_title(self, obj):
        return obj.link_comment.title_of_post
    get_post_title.short_description = 'Публикация'

# Промежуточная таблица связи
@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
