import django_filters

from core.models import Property

class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            'title':['istartswith'],
            'city':['icontains'],
            'check_in_time':['lt', 'gt'],
            'check_out_time':['lt', 'gt'], 
            'guests':['icontains']
            }

class ListFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            'title': ['istartswith']
        }
