from django.contrib import admin
import datetime

from .models import AdvUser, SuperRubric
from .services import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    """ Sending emails with activation requirements
    """
    for person in queryset:
        if not person.is_activated:
            send_activation_notification(person)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')


class NonActivatedFilter(admin.SimpleListFilter):
    """ Checking the user who did not perform the activation
    """
    title = 'Прошли активацию?'
    parameter_name = 'actState'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threeDays', 'Нрошло не более трёх дней'),
            ('week', 'Прошло не более недели'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif value == 'threeDays':
            day = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_acivated=False, is_activated=False, date_joined__data__lt=day)
        elif value == 'week':
            d_time = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_acivated=False, is_activated=False, date_joined__data__lt=d_time)


class AdvUserAdmin(admin.ModelAdmin):
    """ Supportive class
    """
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonActivatedFilter,)
    fields = ('password', ('username', 'email'), ('first_name', 'last_name'), ('is_active', 'is_activated'),
              'groups', 'user_permissions', ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


class SuperRubricInline(admin.TabularInline):
    """ Built-in rubric editor
    """
    model = SuperRubric


class SuperRubricAdmin(admin.ModelAdmin):
    """ Main rubric editor
    """
    exclude = ('super_rubric',)
    inlines = (SuperRubricInline,)


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
