from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели "Автор" в административной панели.
    Обеспечивает удобный просмотр и поиск авторов по имени пользователя.
    """
    list_display = ('user', 'rating')
    search_fields = ('user__username',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели "Категория" в административной панели.
    Позволяет искать категории по названию.
    """
    list_display = ('name_category',)
    search_fields = ('name_category',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели "Публикация" в административной панели.
    Включает отображение ключевых полей, фильтрацию по типу, автору и дате создания,
    а также поиск по заголовку и тексту.
    """
    list_display = ('title_of_post', 'author', 'choice', 'data_created', 'rating_of_post')
    list_filter = ('choice', 'author', 'data_created')
    search_fields = ('title_of_post', 'text_of_post')
    date_hierarchy = 'data_created'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели "Комментарий" в административной панели.
    """
    list_display = ('author_of_comment', 'link_comment', 'date_of_comment', 'rating_of_comment')
    list_filter = ('date_of_comment', 'author_of_comment')
    search_fields = ('comment_text',)
    date_hierarchy = 'date_of_comment'

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    """
    Настройки отображения промежуточной таблицы "Категория поста" в административной панели.
    """
    list_display = ('post', 'category')
