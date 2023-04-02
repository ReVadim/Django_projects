from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    """ Simple tag that return count of published posts
    """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """ Display the latest posts in the sidebar of the blog
    """
    latest_posts = Post.published.order_by('-publish')[:count]

    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """ Display tag with most commented posts
    """
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """ Custom filter to use Markdown syntax in blog posts
    """
    return mark_safe(markdown.markdown(text))
