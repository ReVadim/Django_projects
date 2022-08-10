from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    """ Comments class to display on the admin panel
    """
    model = Comment
    list_display = ('__str__', 'is_active', 'author', 'created_at', 'content',)
    search_fields = ('author', 'is_active', 'created_at',)
    fields = (('username', 'content'), ('created_at', 'is_active'),)
    readonly_fields = ('author', 'content')


admin.site.register(CommentAdmin)
