from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import PostCategory, Category

from django.urls import reverse
from django.conf import settings

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    # Добавляем нового пользователя в группу common
    common_group, created = Group.objects.get_or_create(name='common')
    user.groups.add(common_group)

@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_about_new_post(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        # Получаем только добавленные категории
        categories = Category.objects.filter(pk__in=pk_set)

        # Собираем всех подписчиков из этих категорий
        subscribers = set()
        for category in categories:
            for subscriber in category.subscribers.all():
                if subscriber.email:
                    subscribers.add(subscriber)

        # Отправляем письма каждому подписчику
        for subscriber in subscribers:
            subject = f'Новая статья в подписках: {instance.title_of_post}'
            # Формируем URL (предполагаем, что сайт развернут локально, для реального прода нужен SITE_ID или ALLOWED_HOSTS)
            url = f'http://127.0.0.1:8000{reverse("news_detail", args=[instance.id])}'

            message = (
                f'Здравствуйте, {subscriber.username}!\n\n'
                f'В одной из ваших любимых категорий появилась новая статья: "{instance.title_of_post}".\n'
                f'Краткое содержание: {instance.post_preview()}\n\n'
                f'Читать статью полностью: {url}'
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[subscriber.email],
                fail_silently=True,
            )

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать на News Portal!'
        message = f'Здравствуйте, {instance.username}!\n\nВы успешно зарегистрировались на нашем новостном портале. Спасибо, что вы с нами!'

        # Если email пустой (хотя allauth по идее запрашивает), не отправляем
        if instance.email:
            send_mail(
                subject=subject,
                message=message,
                from_email=None,  # будет использовать DEFAULT_FROM_EMAIL из settings.py
                recipient_list=[instance.email],
                fail_silently=True,
            )
