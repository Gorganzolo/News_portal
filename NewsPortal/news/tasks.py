from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.urls import reverse
from .models import Post, Category
from django.contrib.auth.models import User

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

            for post in posts:
                url = f'http://127.0.0.1:8000{reverse("news_detail", args=[post.id])}'
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
