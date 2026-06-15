from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.urls import reverse
from .models import Post, Category
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings

@shared_task
def send_new_post_notification(post_id, category_ids):
    try:
        post = Post.objects.get(id=post_id)
        categories = Category.objects.filter(id__in=category_ids)
    except Post.DoesNotExist:
        return

    # Собираем всех подписчиков из этих категорий
    subscribers = set()
    for category in categories:
        for subscriber in category.subscribers.all():
            if subscriber.email:
                subscribers.add(subscriber)

    if not subscribers:
        return

    domain = Site.objects.get(id=settings.SITE_ID).domain
    url = f'http://{domain}{reverse("news_detail", args=[post.id])}'

    subject = f'Новая статья в подписках: {post.title_of_post}'

    for subscriber in subscribers:
        message = (
            f'Здравствуйте, {subscriber.username}!\n\n'
            f'В одной из ваших любимых категорий появилась новая статья: "{post.title_of_post}".\n'
            f'Краткое содержание: {post.post_preview()}\n\n'
            f'Читать статью полностью: {url}'
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[subscriber.email],
            fail_silently=True,
        )

@shared_task
def send_welcome_email_task(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return

    if user.email:
        subject = 'Добро пожаловать на News Portal!'
        message = f'Здравствуйте, {user.username}!\n\nВы успешно зарегистрировались на нашем новостном портале. Спасибо, что вы с нами!'

        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[user.email],
            fail_silently=True,
        )

@shared_task
def weekly_newsletter():
    # Определяем период: последние 7 дней
    today = timezone.now()
    last_week = today - timedelta(days=7)

    # Собираем всех пользователей, у которых есть email
    users_with_email = User.objects.exclude(email='')

    for user in users_with_email:
        # Находим категории, на которые подписан пользователь
        user_categories = Category.objects.filter(subscribers=user)

        if not user_categories.exists():
            continue

        # Находим посты в этих категориях за последнюю неделю
        posts = Post.objects.filter(
            category__in=user_categories,
            data_created__gte=last_week
        ).distinct()

        if posts.exists():
            subject = 'Еженедельный дайджест новых статей'

            # Формируем текст письма
            message_lines = [f'Здравствуйте, {user.username}!\n', 'Новые статьи в ваших любимых категориях за прошедшую неделю:\n']

            domain = Site.objects.get(id=settings.SITE_ID).domain

            for post in posts:
                url = f'http://{domain}{reverse("news_detail", args=[post.id])}'
                message_lines.append(f'- {post.title_of_post}')
                message_lines.append(f'  Читать: {url}\n')

            message = '\n'.join(message_lines)

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
