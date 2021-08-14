import django_filters
from .models import CompanyModel


class CompanyFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = CompanyModel
        fields = ['added_by', 'company_name', 'mobile', 'created_at', ]
