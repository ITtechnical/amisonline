import django_filters
from django import forms
from django_filters import DateFilter , CharFilter, NumberFilter
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class TicketFilter(django_filters.FilterSet):
    id = CharFilter(field_name='id',lookup_expr='exact',label='Ticket Id')
    start_date =DateFilter(field_name="ticket_date",lookup_expr='gte',label='Start Date',
                           widget=DateInput(
                               attrs={
                                   'class': 'datepicker'
                               }
                           )

                           )

    end_date =DateFilter(field_name="ticket_date",lookup_expr='gte',label='End Date',
                           widget=DateInput(
                               attrs={
                                   'class': 'datepicker'
                               }
                           )

                           )

    class Meta:
        model = Ticket
        fields = ['start_date','end_date','status', 'prority','escalated','category','id','region','agent_team','agent','escalated']
