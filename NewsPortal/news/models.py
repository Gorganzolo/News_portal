from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Модель категорий
class Category(models.Model):
    name_category = models.CharField(verbose_name='Название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name_category


# Модель автора
class Author(models.Model):
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.user.username

    def update_rating(self):
        """Обновляет рейтинг автора по постам и комментариям"""
        sum_rating_of_post = self.post_set.aggregate(Sum('rating_of_post'))['rating_of_post__sum'] or 0
        sum_rating_of_post *= 3
        sum_rating_of_comment = self.user.comment_set.aggregate(Sum('rating_of_comment'))['rating_of_comment__sum'] or 0
        sum_rating_of_comment_on_post = Comment.objects.filter(link_comment__author=self).aggregate(Sum('rating_of_comment'))['rating_of_comment__sum'] or 0
        self.rating = sum_rating_of_post + sum_rating_of_comment + sum_rating_of_comment_on_post
        self.save()

# Модель поста (новость/статья)
class Post(models.Model):

    article = 'AR'
    news = 'NW'

    CATEGORY_CHOICES = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    data_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, verbose_name='Категория', through='PostCategory')
    choice = models.CharField(verbose_name='Вид поста', max_length=2, choices=CATEGORY_CHOICES, default=article)
    title_of_post= models.CharField(verbose_name='Название', max_length=100)
    text_of_post = models.TextField(verbose_name='Текст поста')
    rating_of_post = models.IntegerField(verbose_name='Рейтинг', default=0)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title_of_post

    def like(self):
        """Лайк посту"""
        self.rating_of_post += 1
        self.save()

    def dislike(self):
        """Дизлайк посту"""
        self.rating_of_post -= 1
        self.save()

    def post_preview(self):
        """Предпросмотр текста поста"""
        return self.text_of_post[:124] + "..."


# Модель комментария
class Comment(models.Model):
    link_comment = models.ForeignKey('Post', verbose_name='Пост', on_delete=models.CASCADE)
    author_of_comment = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    comment_text = models.TextField(verbose_name='Текст')
    date_of_comment = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    rating_of_comment = models.IntegerField(verbose_name='Рейтинг', default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.comment_text[:20]

    def like(self):
        """Лайк комментарию"""
        self.rating_of_comment += 1
        self.save()

    def dislike(self):
        """Дизлайк комментарию"""
        self.rating_of_comment -= 1
        self.save()


# Промежуточная модель связи поста и категории
class PostCategory(models.Model):
    post = models.ForeignKey('Post', verbose_name='Пост', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория поста'
        verbose_name_plural = 'Категории постов'
