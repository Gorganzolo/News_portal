import django_filters
from django.forms import DateInput
from .models import Post

class PostFilter(django_filters.FilterSet):
    # Фильтр по названию
    title_of_post = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Название содержит'
    )
    # Фильтр по имени автора (через User)
    author__user__username = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Имя автора содержит'
    )
    # Фильтр по дате создания (позже или равно указанной)
    data_created = django_filters.DateFilter(
        lookup_expr='gte',
        label='Дата (начиная с)',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title_of_post', 'author__user__username', 'data_created']
