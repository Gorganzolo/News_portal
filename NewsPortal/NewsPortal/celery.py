import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем модуль настроек Django по умолчанию для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')

# Используем строку для конфигурации, чтобы воркеру не нужно было сериализовать объект конфигурации
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загружаем задачи (tasks.py) из всех зарегистрированных Django приложений
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weekly_newsletter': {
        'task': 'news.tasks.weekly_newsletter',
        # Каждую неделю в понедельник в 8 утра
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
