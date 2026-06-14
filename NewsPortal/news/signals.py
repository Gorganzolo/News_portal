from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    # Добавляем нового пользователя в группу common
    common_group, created = Group.objects.get_or_create(name='common')
    user.groups.add(common_group)
