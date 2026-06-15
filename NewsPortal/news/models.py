from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Категории новостей/статей
class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name_category

# Автор (связан с пользователем)
class Author(models.Model):
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

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

# Пост (новость или статья)
class Post(models.Model):

    article = 'AR'
    news = 'NW'

    CATEGORY_CHOICES = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    data_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категории')
    choice = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=article, verbose_name='Тип поста')
    title_of_post= models.CharField(max_length=100, verbose_name='Заголовок')
    text_of_post = models.TextField(verbose_name='Текст поста')
    rating_of_post = models.IntegerField(default=0, verbose_name='Рейтинг поста')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

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


# Комментарий к посту
class Comment(models.Model):
    link_comment = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Пост')
    author_of_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    comment_text = models.TextField(verbose_name='Текст комментария')
    date_of_comment = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    rating_of_comment = models.IntegerField(default=0, verbose_name='Рейтинг комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        """Лайк комментарию"""
        self.rating_of_comment += 1
        self.save()

    def dislike(self):
        """Дизлайк комментарию"""
        self.rating_of_comment -= 1
        self.save()


# Связь поста и категории
class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Пост')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = 'Связь Пост-Категория'
        verbose_name_plural = 'Связи Пост-Категория'
