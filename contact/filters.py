import django_filters
from .models import ContactModel, LeadsModel


class ContactFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    mobile = django_filters.CharFilter(lookup_expr='icontains')
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = ContactModel
        fields = '__all__'


class LeadFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    mobile = django_filters.CharFilter(lookup_expr='icontains')
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = LeadsModel
        fields = ['name', 'mobile', 'type', 'added_by', 'created_at', ]
