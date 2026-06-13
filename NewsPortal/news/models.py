from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.

class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True)


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        sum_rating_of_post = self.post_set.aggregate(Sum('rating_of_post'))['rating_of_post__sum']
        sum_rating_of_post *= 3
        sum_rating_of_comment = self.user.comment_set.aggregate(Sum('rating_of_comment'))['rating_of_comment__sum'] or 0
        sum_rating_of_comment_on_post = Comment.objects.filter(link_comment__author=self).aggregate(Sum('rating_of_comment'))['rating_of_comment__sum'] or 0
        self.rating = sum_rating_of_post + sum_rating_of_comment + sum_rating_of_comment_on_post
        self.save()

class Post(models.Model):

    article = 'AR'
    news = 'NW'

    CATEGORY_CHOICES = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    data_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    choice = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=article)
    title_of_post= models.CharField(max_length=100)
    text_of_post = models.TextField()
    rating_of_post = models.IntegerField(default=0)

    def like(self):
        self.rating_of_post += 1
        self.save()
    def dislike(self):
        self.rating_of_post -= 1
        self.save()

    def post_preview(self):
        return self.text_of_post[:124] + "..."


class Comment(models.Model):
    link_comment = models.ForeignKey('Post', on_delete=models.CASCADE)
    author_of_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_of_comment = models.DateTimeField(auto_now_add=True)
    rating_of_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_of_comment += 1
        self.save()
    def dislike(self):
        self.rating_of_comment -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)




