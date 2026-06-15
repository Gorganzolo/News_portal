from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from .models import PostCategory

from .tasks import send_new_post_notification, send_welcome_email_task

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    # Добавляем нового пользователя в группу common
    common_group, created = Group.objects.get_or_create(name='common')
    user.groups.add(common_group)

@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_about_new_post(sender, instance, action, pk_set, **kwargs):
    # Если reverse=True, значит мы добавляем со стороны Category (через reverse relation),
    # тогда instance - это Category, а не Post, и у него нет title_of_post.
    # Так как мы ожидаем, что посты добавляются через форму или админку к посту,
    # мы игнорируем reverse добавления для безопасности.
    if action == 'post_add' and not kwargs.get('reverse'):
        # Передаем id поста и id добавленных категорий в асинхронную задачу Celery
        send_new_post_notification.delay(instance.id, list(pk_set))

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # Запускаем отправку письма асинхронно
        send_welcome_email_task.delay(instance.id)
