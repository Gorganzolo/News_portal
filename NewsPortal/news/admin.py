from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory

# Регистрируем модели в админке для удобного управления
# Добавлены понятные лейблы, фильтры и поиск, всё переведено на русский

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Автор в панели администратора.
    """
    list_display = ('user', 'rating')
    search_fields = ('user__username',)
    # Имена для полей в списке
    user_label = 'Пользователь'
    rating_label = 'Рейтинг'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Категория в панели администратора.
    """
    list_display = ('name_category',)
    search_fields = ('name_category',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Публикация (Новость/Статья) в панели администратора.
    Обеспечивает удобный поиск по заголовку и тексту, а также фильтрацию по типу, автору и дате.
    """
    list_display = ('title_of_post', 'author', 'get_choice_display', 'data_created', 'rating_of_post')
    list_filter = ('choice', 'author', 'data_created')
    search_fields = ('title_of_post', 'text_of_post')
    date_hierarchy = 'data_created'

    @admin.display(description='Тип')
    def get_choice_display(self, obj):
        return obj.get_choice_display()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели Комментарий в панели администратора.
    """
    list_display = ('author_of_comment', 'get_short_text', 'link_comment', 'date_of_comment', 'rating_of_comment')
    list_filter = ('date_of_comment', 'author_of_comment')
    search_fields = ('comment_text',)
    date_hierarchy = 'date_of_comment'

    @admin.display(description='Текст комментария')
    def get_short_text(self, obj):
        # Показываем только первые 50 символов в админке
        if len(obj.comment_text) > 50:
            return f"{obj.comment_text[:50]}..."
        return obj.comment_text

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    """
    Настройки отображения промежуточной таблицы связи Публикации и Категории.
    """
    list_display = ('post', 'category')
    search_fields = ('post__title_of_post', 'category__name_category')
