from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post

class Command(BaseCommand):
    help = 'Создает группы common и authors, выдает необходимые права.'

    def handle(self, *args, **options):
        common_group, created = Group.objects.get_or_create(name='common')
        authors_group, created = Group.objects.get_or_create(name='authors')

        content_type = ContentType.objects.get_for_model(Post)
        add_permission = Permission.objects.get(codename='add_post', content_type=content_type)
        change_permission = Permission.objects.get(codename='change_post', content_type=content_type)

        authors_group.permissions.add(add_permission, change_permission)

        self.stdout.write(self.style.SUCCESS('Группы и права успешно настроены.'))
