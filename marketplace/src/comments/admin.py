from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    """ Comments class to display on the admin panel
    """
    model = Comment
    list_display = ('__str__', 'is_active', 'author', 'created_at', 'content', 'advertisement',)
    search_fields = ('author', 'is_active', 'created_at',)
    fields = (('author', 'content'), ('advertisement', 'is_active'), 'created_at',)
    readonly_fields = ('created_at',)


admin.site.register(Comment, CommentAdmin)
