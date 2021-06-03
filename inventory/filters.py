import django_filters
from .models import *


class BorrowFilter(django_filters.FilterSet):
    class Meta:
        model = Borrow
        fields = ['user', 'book']
