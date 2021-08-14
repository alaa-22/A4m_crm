import django_filters
from django.contrib.auth.models import User
from .models import Log


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', 'email', 'date_joined', 'is_active']


class LogFilter(django_filters.FilterSet):

    class Meta:
        model = Log
        fields = ['user', 'action', ]
