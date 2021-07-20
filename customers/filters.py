import django_filters
from .models import Customer

class CustomerFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='iexact')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='iexact')
    email = django_filters.CharFilter(field_name='email', lookup_expr='iexact')
    address = django_filters.CharFilter(field_name='address', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='iexact')
    state = django_filters.CharFilter(field_name='state', lookup_expr='iexact')
    zip = django_filters.CharFilter(field_name='zip', lookup_expr='iexact')

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'state', 'zip']