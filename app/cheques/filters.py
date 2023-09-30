import django_filters
from django import forms

from .models import Cheque


class ChequeFilter(django_filters.FilterSet):
    date_debited = django_filters.DateFromToRangeFilter(
        field_name="date_debited",
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'})
    )

    class Meta:
        model = Cheque
        fields = [
            "date_debited",
        ]
