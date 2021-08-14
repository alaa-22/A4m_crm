import django_filters
from .models import TaskModel, WhatsappModel, SendEmailModel, MeetingModel, ActivityModel


class WhatsappFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = WhatsappModel
        fields = ['contact_person', 'phone', 'made_by']


class TaskFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = TaskModel
        fields = '__all__'
        exclude = ['subject',  'made_by',]


class MailFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = SendEmailModel
        fields = '__all__'
        exclude = ['subject', 'message', 'file']


class Meeting(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = MeetingModel
        fields = ['contact_person', 'date', 'made_by']


class ActivityFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = ActivityModel
        fields = ['type', 'created_at', 'made_by']


class Activity_ReportFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = ActivityModel
        fields = '__all__'
