from django_filters import rest_framework as filters

from .models import Survey


class AnswerFilter(filters.FilterSet):
    """ Filter class for answers """

    class Meta:
        model = Survey
        fields = ['start_time', 'end_time', 'is_active']
