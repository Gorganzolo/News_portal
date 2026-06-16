from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Модель для категорий новостей/статей
class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True, verbose_name="Подписчики")

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

# Модель автора (связан с пользователем Django)
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг автора")

    def update_rating(self):
        """Обновляет рейтинг автора по постам и комментариям"""
        sum_rating_of_post = self.post_set.aggregate(Sum('rating_of_post'))['rating_of_post__sum'] or 0
        sum_rating_of_post *= 3
        sum_rating_of_comment = self.user.comment_set.aggregate(Sum('rating_of_comment'))['rating_of_comment__sum'] or 0
        sum_rating_of_comment_on_post = Comment.objects.filter(link_comment__author=self).aggregate(Sum('rating_of_comment'))['rating_of_comment__sum'] or 0
        self.rating = sum_rating_of_post + sum_rating_of_comment + sum_rating_of_comment_on_post
        self.save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

# Модель для публикаций (новостей и статей)
class Post(models.Model):
    article = 'AR'
    news = 'NW'

    CATEGORY_CHOICES = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    choice = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=article, verbose_name="Тип публикации")
    data_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name="Категории")
    title_of_post = models.CharField(max_length=100, verbose_name="Заголовок")
    text_of_post = models.TextField(verbose_name="Текст")
    rating_of_post = models.IntegerField(default=0, verbose_name="Рейтинг")

    def like(self):
        """Увеличивает рейтинг поста"""
        self.rating_of_post += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг поста"""
        self.rating_of_post -= 1
        self.save()

    def post_preview(self):
        """Возвращает предпросмотр текста поста (первые 124 символа)"""
        return self.text_of_post[:124] + "..."

    def __str__(self):
        return self.title_of_post

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

# Модель комментария к посту
class Comment(models.Model):
    link_comment = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Публикация")
    author_of_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    comment_text = models.TextField(verbose_name="Текст комментария")
    date_of_comment = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating_of_comment = models.IntegerField(default=0, verbose_name="Рейтинг")

    def like(self):
        """Увеличивает рейтинг комментария"""
        self.rating_of_comment += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг комментария"""
        self.rating_of_comment -= 1
        self.save()

    def __str__(self):
        return f"{self.author_of_comment.username} к {self.link_comment.title_of_post}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

# Промежуточная модель связи поста и категории
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Публикация")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория публикации"
        verbose_name_plural = "Категории публикаций"
